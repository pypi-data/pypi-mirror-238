## Work Items

1. integrate with huggingface pretrained models

2. underflow with matrix multiplication (need a repro first)

3. (***) streaming data interface
4. connectors to other data sources
5. flexibility with model specification (onnx, auto-detect second last layer)

6. auto-tune batch sizes, other parameters

7. performance of the library
8. add ci and tests

9. azureml template


TODO:
x1. pretrained model interface design
x2. classification model
x3. get_embedding_dim
x4. nLabs
x5. demo using pretrained model
6. underflow repro -- n_start 40k, batch size 1k ==> undersample than the budget
7. streaming interface