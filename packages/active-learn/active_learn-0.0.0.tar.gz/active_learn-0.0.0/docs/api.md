# API Overview

~~~ python
from active_learn import ActiveSampler

sampler = ActiveSampler("classification", model, budget=1000)  # Returns an "active learning" sampler
valuable_data_set = sampler.select(candidate_data_set)  # Chooses N best samples to label and learn from
~~~


## Sampler Initialization

~~~ python
class ActiveSampler(problem_type, model, budget, precompute_covariance=False, seed_fisher=False)
~~~

Initializes active learn object, allows user to specify relevant hyperparameters.

| Parameter | Type | Description | Default | Example Value |
|-----------|------|-------------|---------|---------------|
| problem_type | str | 'classification' or 'regression' | None | 'classification' |
| model | ONNX or pytorch object, (model, tokenizer) tuple for transformer | Neural network model and corresponding tokenizer if necessary | None | nn.Sequential object, huggingface tokenizer if necessary |
| budget | int or float | Labeling budget / acceptable labeling frequency (if total number of samples is not known) | None | 100 or 0.1 |
| labeled_data | Tensor, numpy array, list | Samples that have been used for training the model | None | |
| precompute_covariance | bool | Toggles whether to first loop over all data to compute their empirical covariance. In streaming settings this is computed on the fly, but if possible it may be better to precompute | | |
| seed_fisher | bool | Explicitly conditions sampling on data that have already been used to train the model. Makes more difference for regression problems. | | |


## Active Selection

~~~ python
sampler.select(X_candidates)
~~~

Performs active selection using the internal selection parameters that are either found by hyperparameter_tune or are manually set. Returns a budget number (or budget fraction) of samples taken from X_candidates to have been labeled by an external entity.

| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| X_candidates | Tensor or numpy array, or pipe | Pool of data from which to select important instances | None |
