from transformers import PreTrainedModel
import torch
import types


# mention hf in func name
def get_active_model(model):
    assert isinstance(model, torch.nn.Module)
    assert isinstance(model, PreTrainedModel)
    # print(type(model))
    # print(model.__class__.__name__)
    assert model.__class__.__name__.endswith("SequenceClassification")  # TODO

    def get_embedding_dim(self):
        # TODO: all classification models have score?
        return self.score.weight.shape[-1]

    def get_outputs_and_embeddings(self, tokenized_inputs):
        input_ids = torch.LongTensor(tokenized_inputs["input_ids"])
        attn_mask = torch.Tensor(tokenized_inputs["attention_mask"])
        self.eval()
        with torch.no_grad():
            outputs = self(
                input_ids=input_ids,
                attention_mask=attn_mask,
                output_hidden_states=True,
            )

        activations = outputs.hidden_states
        ll_activations = activations[-1]
        pad = self.config.pad_token_id
        # TODO: Handle padding_side (below only works for padding right).
        last_token_inds = torch.ne(input_ids, pad).sum(-1) - 1
        embeddings = ll_activations[
            torch.arange(len(last_token_inds)), last_token_inds, :
        ]

        # Sanity check that the embeddings generates the correct logits.
        manual_logits = embeddings @ self.score.weight.t()
        assert torch.all(manual_logits == outputs.logits)

        return outputs.logits, embeddings

    # Bind the methods to the model object.
    model.get_embedding_dim = types.MethodType(get_embedding_dim, model)
    model.get_outputs_and_embeddings = types.MethodType(
        get_outputs_and_embeddings, model
    )

    return model
