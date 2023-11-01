from copy import copy as copy
from copy import deepcopy as deepcopy

import numpy as np
import torch
from torch.nn import functional as F


def _inf_replace(mat):
    mat[torch.where(torch.isinf(mat))] = (
        torch.sign(mat[torch.where(torch.isinf(mat))]) * np.finfo("float32").max
    )
    return mat


# Streaming sampling (like VeSSAL)
def _streaming_sampling(
    samps,
    k,
    labeled_cov_inv,
    labeled_cov,
    early_stop=False,
    total_covariance=None,
    labels_used=0,
):
    inds = []
    skipped_inds = []

    rank = samps.shape[-2]

    covariance = labeled_cov.cuda()  # covariance over all samples
    covariance_inv = labeled_cov_inv.cuda()  # inverse covariance over selected samples
    samps = torch.tensor(samps)
    samps = samps.cuda()

    if total_covariance != None:
        covariance = total_covariance

    print("Start sampling ...")
    for i, u in enumerate(samps):
        # TODO: Log progress.
        # if i % 1000 == 0:
        #     print(i, len(inds), flush=True)
        if rank > 1:
            u = torch.Tensor(u).t().cuda()
        else:
            u = u.view(-1, 1)

        # get determinantal contribution (matrix determinant lemma)
        if rank > 1:
            norm = torch.abs(torch.det(u.t() @ covariance_inv @ u))
        else:
            norm = torch.abs(u.t() @ covariance_inv @ u)

        ideal_rate = (k - len(inds)) / (len(samps) - (i))

        # just average everything together: \Sigma_t = (t-1)/t * A\{t-1}  + 1/t * x_t x_t^T
        t = labels_used + i
        if total_covariance == None:
            # TODO: could be underflow in u u^T if u has small values
            # elevate precision, clamping min value
            covariance = (t / (t + 1)) * covariance + (1 / (t + 1)) * (u @ u.t())

        zeta = (ideal_rate / (torch.trace(covariance @ covariance_inv))).item()

        pu = np.abs(zeta) * norm

        if np.random.rand() < pu.item():
            inds.append(i)
            if early_stop and len(inds) >= k:
                break

            # woodbury update to covariance_inv
            inner_inv = torch.inverse(
                torch.eye(rank).cuda() + u.t() @ covariance_inv @ u
            )
            inner_inv = _inf_replace(inner_inv)
            covariance_inv = (
                covariance_inv - covariance_inv @ u @ inner_inv @ u.t() @ covariance_inv
            )
        else:
            skipped_inds.append(i)

    # fill in any remaining budget with random (shouldn't happen often)
    while len(inds) < k:
        ind = np.random.randint(len(samps))
        if ind not in inds:
            inds.append(ind)

    print("Sampling done")
    return inds


# TODO: ActiveSamplerArguments for all hyperparams?
# TODO: This only handles data as numpy arrays
# TODO: This expects pytorch models, locally stored, and doesn't do anything clever to auto-detect layers needed for sampling
class ActiveSampler:
    def __init__(
        self,
        problem_type,
        model,
        budget,
        labeled_data=(),
        rank=1,
        precompute_covariance=False,
        seed_fisher=False,
        lamb=1e-2,
    ):
        # TODO: Add error messages, or use get_active_model over PreTrainedModels.
        assert hasattr(model, "get_embedding_dim")
        assert hasattr(model, "get_outputs_and_embeddings")

        self.problem_type = problem_type
        self.budget = budget
        self.model = model
        self.rank = rank
        self.seed_fisher = seed_fisher
        self.lamb = lamb
        self.labeled_data = labeled_data
        self.precompute_covariance = precompute_covariance
        self.seed_fisher = seed_fisher

    # gets gradient embeddings for classification problems (assumes cross-entropy loss)
    def _get_grad_embedding(self, X):
        embDim = self.model.get_embedding_dim()
        self.model.eval()

        if hasattr(self.model, "score"):
            nLab = self.model.score.out_features
        elif hasattr(self.model, "linear"):
            nLab = self.model.linear.out_features
        else:
            # TODO: Add error message.
            assert False
        embedding = np.zeros([len(X), self.rank, embDim * nLab])

        ## TODO: auto-detect maximum batch_size
        batch_size = 1000  # should be as large as gpu memory allows
        n_samps = len(X)
        rounds = int(np.ceil(n_samps / batch_size))
        for ind in range(self.rank):
            with torch.no_grad():
                for i in range(rounds):
                    inds = np.arange(i * batch_size, min((i + 1) * batch_size, n_samps))

                    # TODO:
                    if isinstance(X, np.ndarray):
                        x = torch.Tensor(X[inds]).cuda()
                        out, emb = self.model.get_outputs_and_embeddings(x)
                    else:
                        tokenized_inputs = {"input_ids": [], "attention_mask": []}
                        for idx in inds:
                            tokenized_inputs["input_ids"].append(X[idx]["input_ids"])
                            tokenized_inputs["attention_mask"].append(
                                X[idx]["attention_mask"]
                            )
                        out, emb = self.model.get_outputs_and_embeddings(
                            tokenized_inputs
                        )

                    emb = emb.data.cpu().numpy()
                    batchProbs = F.softmax(out, dim=1).data.cpu().numpy()

                    for j in range(len(inds)):
                        order = np.argsort(batchProbs[j])[::-1]
                        probs = batchProbs[j][order]
                        for c in range(nLab):
                            if c == ind:
                                embedding[inds[j]][ind][
                                    embDim * c : embDim * (c + 1)
                                ] = deepcopy(emb[j]) * (1 - probs[c])
                            else:
                                embedding[inds[j]][ind][
                                    embDim * c : embDim * (c + 1)
                                ] = deepcopy(emb[j]) * (-1 * probs[c])
                        probs = probs / np.sum(probs)
                        embedding[inds[j]][ind] = embedding[inds[j]][ind] * np.sqrt(
                            probs[ind]
                        )
        return torch.Tensor(embedding)

    # gets penultimate-layer embeddings for regression
    def _get_penultimate_embedding(self, X):
        self.model.eval()
        embedding = torch.zeros([len(X), self.model.get_embedding_dim()])
        n_samps = len(X)
        batch_size = 1000
        rounds = int(np.ceil(n_samps / batch_size))
        with torch.no_grad():
            for i in range(rounds):
                inds = np.arange(i * batch_size, min((i + 1) * batch_size, n_samps))
                x = torch.Tensor(X[inds]).cuda()
                _, e1 = self.model.get_outputs_and_embeddings(x)
                embedding[inds] = e1.data.cpu()
        return embedding

    def select(self, X_candidates):
        batchSize = 1000  # should be as large as GPU memory allows
        X_labeled = self.labeled_data

        ## TODO: only compute embedding labels if they are provided and if sampling is conditioned on them
        if self.problem_type == "classification":
            emb_candidates = self._get_grad_embedding(X_candidates)
            emb_labeled = self._get_grad_embedding(X_labeled)
        else:
            emb_candidates = self._get_penultimate_embedding(X_candidates)
            emb_labeled = self._get_penultimate_embedding(X_labeled)

        dim = emb_candidates.shape[-1]

        # initialize fisher and inverse over all labeled samples
        labeled_cov = torch.zeros(dim, dim).cuda()
        labeled_cov_inv = torch.eye(dim, dim).cuda() * self.lamb**-1
        n_candidates = len(X_candidates)
        n_labeled = len(X_labeled)
        labels_used = 0
        if self.seed_fisher:
            labels_used = n_labeled
            for i in range(int(np.ceil(n_labeled / batchSize))):
                embs = emb_labeled[i * batchSize : (i + 1) * batchSize].cuda()

                # the non-inverted covariance matrix is used to compute an expectation, so it's normalized
                labeled_cov = (
                    labeled_cov
                    + (torch.bmm(embs.transpose(1, 2), embs).detach()).sum(0)
                    / n_labeled
                )

                # update inverse (woodbury update - more numerically stable and quadratic (instead of cubic) update)
                embs = embs.squeeze()
                rank = len(embs)
                inner_inv = torch.inverse(
                    torch.eye(rank).cuda() + embs @ labeled_cov_inv @ embs.t()
                ).detach()
                labeled_cov_inv = (
                    labeled_cov_inv @ embs.t() @ inner_inv @ embs @ labeled_cov_inv
                ).detach()

        # take a pass over all data to precompute relevant statistics (the covariance matrix over all data)
        total_covariance = None
        if self.precompute_covariance:
            total_covariance = torch.zeros(dim, dim).cuda()
            all_embs = torch.concatenate((emb_candidates, emb_labeled))
            for i in range(int(np.ceil((n_candidates + n_labeled) / batchSize))):
                embs = all_embs[i * batchSize : (i + 1) * batchSize].cuda()

                ## TODO: if embs has small values, then underflow might happen, could damage sampling quality
                total_covariance = total_covariance + (
                    torch.bmm(embs.transpose(1, 2), embs).detach()
                ).sum(0) / (n_candidates + n_labeled)

        # streaming sampling
        chosen = _streaming_sampling(
            emb_candidates,
            self.budget,
            labeled_cov_inv,
            labeled_cov,
            total_covariance=total_covariance,
            labels_used=labels_used,
        )
        return chosen
