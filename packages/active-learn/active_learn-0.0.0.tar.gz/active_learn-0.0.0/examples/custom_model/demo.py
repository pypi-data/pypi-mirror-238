# TODO: Convert to a notebook.

import argparse
import sys

# TODO: naming - active_learn, active-learn, ActiveLearn, activeml, deep_active, ...
# https://peps.python.org/pep-0008/#naming-conventions
from active_learn import ActiveSampler

import numpy as np
import torch
import wandb
from sklearn.model_selection import train_test_split
from torchvision import transforms

# TODO: Refactor dataset, resnet & vgg.
from models import mlp, resnet, vgg
from dataset import get_dataset, get_handler


def parse_args():
    parser = argparse.ArgumentParser()

    # ActiveSampler parameters.
    parser.add_argument(
        "--problem_type",
        help="classification or regression",
        type=str,
        default="classification",
    )
    parser.add_argument(
        "--budget",
        help="number of points to query at a time",  # TODO: Add support for float rates for streaming inputs.
        type=int,
        default=1000,
    )
    parser.add_argument(
        "--precompute_covariance",
        help="precomputes covariance matrix for more accurate data selection (requires taking two passes over data, not possible in true streaming situations)",
        action="store_true",
    )
    parser.add_argument(
        "--seed_fisher",
        help="conditions sampling on data the model has already been trained on",
        action="store_true",
    )

    # Data & model.
    parser.add_argument("--path", help="data path", type=str, default="data")
    parser.add_argument(
        "--model", help="model - resnet, vgg, or mlp", type=str, default="mlp"
    )

    # Addtitional active learning parameters.
    parser.add_argument(
        "--rounds",
        help="number of active learning rounds",
        type=int,
        default=10,
    )
    parser.add_argument(
        "--n_start",
        help="number of points to train initial model with",
        type=int,
        default=1000,
    )
    parser.add_argument(
        "--random_sample",
        help="does random sampling instead, for debugging",
        action="store_true",
    )

    # Other hyperparameters used during training.
    parser.add_argument("--lr", help="learning rate", type=float, default=1e-3)

    return parser.parse_args()


# TODO: Use a local notebook to plot charts.
def init_logger(random_sample: bool):
    # Logging to wandb.
    wandb.login()  # TODO: key
    wandb.init(
        project="active_learning_api",
        name="random" if random_sample else "active",
    )
    # Define x-axis and metrics to be plotted against it.
    wandb.define_metric("train_data")
    wandb.define_metric("eval_accuracy", step_metric="train_data")


# Assumption: torch.nn.Module model returns embedding during forward().
def init_model(model: str):
    # TODO: Don't make assumptions about what is returned from model class
    # TODO: Auto-detect last / penultimate layer
    # TODO: Accept ONNX models, etc.
    if model == "mlp":
        return mlp.MLP(32 * 32 * 3, embSize=128).cuda()
    elif model == "resnet":
        return resnet.ResNet18().cuda()
    elif model == "vgg":
        return vgg.VGG("VGG16").cuda()
    else:
        print("choose a valid model - mlp, resnet, or vgg", flush=True)
        raise ValueError


# TODO: Move this logic into dataset.py.
def prepare_data(data_path: str, n_start: int):
    # TODO: Accept more general data formats, e.g. numpy arrays, lists, tensors
    # TODO: Add support some kind of streaming data
    # TODO: Use huggingface dataset?

    # get some data
    X_tr, Y_tr, _, _ = get_dataset("SVHN", data_path)
    transform = transforms.Compose(
        [
            transforms.ToTensor(),
            transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5)),
        ]
    )

    X, Y = [], []
    for item in get_handler("SVHN")(X_tr, Y_tr, transform=transform):
        X.append(item[0].numpy())
        Y.append(item[1].numpy())
    X = np.stack(X)
    Y = np.stack(Y)

    # make some test data
    X, X_test, Y, Y_test = train_test_split(X, Y, test_size=0.1)

    # make some data to treat as labeled and use the remainder as unlabeled candidates
    X_candidates, X_labeled, Y_candidates, Y_labeled = train_test_split(
        X, Y, test_size=n_start
    )

    return X_candidates, Y_candidates, X_labeled, Y_labeled, X_test, Y_test


# TODO: Refactor, split train & eval.
# define a simple train function
def train(net, X, Y, eval_only=False, verbose=False):
    if not eval_only:

        def weight_reset(m):
            if isinstance(m, torch.nn.Conv2d) or isinstance(m, torch.nn.Linear):
                m.reset_parameters()

        net.apply(weight_reset)

    net = net.cuda().train()
    optimizer = torch.optim.Adam(net.parameters(), lr=args.lr, weight_decay=0)
    batch_size, acc, epoch, n_samps = 128, 0, 0, len(X)

    if eval_only:
        net = net.eval()

    with torch.set_grad_enabled(not eval_only):
        while acc < 0.99:
            acc = 0
            for i in range(int(np.ceil(n_samps / batch_size))):
                optimizer.zero_grad()
                inds = np.arange(i * batch_size, min((i + 1) * batch_size, n_samps))
                x = torch.Tensor(X[inds]).cuda()
                y = torch.LongTensor(Y[inds]).cuda()
                out = net(x)
                acc += torch.sum((torch.max(out, 1)[1] == y).float()).data.item()
                if not eval_only:
                    loss = torch.nn.functional.cross_entropy(out, y)
                    loss.backward()
                    optimizer.step()
            acc /= n_samps
            if eval_only:
                return acc
            epoch += 1
            if verbose:
                print(
                    "epoch: " + str(epoch) + ", training accuracy: " + str(acc),
                    flush=True,
                )

    return net


# TODO: Refactor.
def demo_active_learning_loop(args, model, data):
    X_candidates, Y_candidates, X_labeled, Y_labeled, X_test, Y_test = data

    # train an initial model on labeled data
    net = train(model, X_labeled, Y_labeled)
    initial_accuracy = train(net, X_test, Y_test, eval_only=True)
    print("initial accuracy: " + str(initial_accuracy), flush=True)
    wandb.log({"train_data": len(X_labeled), "eval_accuracy": initial_accuracy})

    for i in range(args.rounds):
        # TODO: re-init model every round?

        if args.random_sample:
            # Random sampling.
            inds = np.random.permutation(len(X_candidates))[: args.budget]

        else:
            # Active learning.

            # set up the sampler
            sampler = ActiveSampler(
                args.problem_type,
                net,
                args.budget,
                labeled_data=X_labeled,
                precompute_covariance=args.precompute_covariance,
                seed_fisher=args.seed_fisher,
            )

            # select samples
            inds = sampler.select(X_candidates)

        # get new data
        X_new = np.concatenate((X_labeled, X_candidates[inds]), 0)
        Y_new = np.concatenate((Y_labeled, Y_candidates[inds]), 0)

        # update model
        net = train(net, X_new, Y_new)
        accuracy = train(net, X_test, Y_test, eval_only=True)
        print("Accuracy", i, len(X_new), accuracy, flush=True)
        wandb.log({"train_data": len(X_new), "eval_accuracy": accuracy})

        # update training data and remove chosen candidates from the pool
        X_labeled = X_new
        Y_labeled = Y_new
        not_chosen = np.asarray([True] * len(X_candidates))
        not_chosen[inds] = False
        X_candidates = X_candidates[not_chosen]
        Y_candidates = Y_candidates[not_chosen]

        if len(X_candidates) < args.budget:
            print("not enough points remain")
            break


if __name__ == "__main__":
    args = parse_args()

    # Initialize logging.
    init_logger(args.random_sample)

    # Load the specified neural net.
    model = init_model(args.model)

    # Load the dataset.
    data = prepare_data(args.path, args.n_start)

    # Run a demo of an active learning loop.
    demo_active_learning_loop(args, model, data)

    sys.exit()
