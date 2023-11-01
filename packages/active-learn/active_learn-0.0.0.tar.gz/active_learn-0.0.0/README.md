# Deep Active Learning Library

## Introduction

Supervised machine learning models are trained to map input data to desired outputs. Often, unlabeled samples are abundant, but obtaining corresponding labels is costly. In particular, acquiring these labels may require human annotators, extensive compute, or a substantial amount of time. In these scenarios, it's best to think carefully about how we allocate these scarce resources, and to prioritize labeling samples that will, once labeled and trained on, facilitate the largest improvements in model quality. The problem of identifying these high-information samples, given a constraint on how much data we are willing to have labeled, is referred to as **_Active Learning_**.

Active learning problems are ubiquitous in practical, real-world machine learning deployments. Building on an array of state-of-the-art algorithms developed in our lab, this library provides a general-purpose tool for active learning with deep neural networks.

![active learning](./docs/active_learning.png)

### Why Does it Matter?

Active learning matters because it allows us to train higher-performing models at a reduced cost. While the potential applications are abundant, the underlying technology is somewhat general, allowing us to build one tool that can handle a wide array of use cases.

One big active learning success at Microsoft involves a Bing language model called "RankLM." RankLM predicts the quality of a search query-result pair, and obtaining these labels for training is costly — requiring either human annotators or compute-intensive models. By using active learning to construct an information-dense training set, the Bing team was able to obtain a significant boost in the predictive quality of RankLM.


## Build & Installation

Users can build a wheel package and use it as follows.

~~~ python
python -m pip install --upgrade build
python -m build

pip install dist/active_learn-*.whl
~~~


## Example Usage

Users can use any `torch.nn` module with the library. See [a demo here](./examples/).

~~~ python
pip install -r examples/requirements.txt
python examples/demo.py
~~~

### Using a pretrained model (TBD)

<!-- TODO: Add a demo for selecting unlabeled samples using a pretrained transformer model. -->

~~~ python
from active_learn import ActiveSampler

import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from datasets import load_dataset

# 1) Load a pretrained sentiment classifier
model_name = "finiteautomata/bertweet-base-sentiment-analysis"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSequenceClassification.from_pretrained(model_name)

# 2) Load a new sentiment dataset unlike what the model was trained on.
#    -
#    Here we're pretending labels are not available, and we want to identify the
#    most useful 'n' samples to send to an expert to have labeled before
#    integrating # them into our training data
sentences = samples['train']['sentence']

# 3) Get 100 most valuable samples
sampler = ActiveSampler('classification', (model, tokenizer), 100)
valuable_samples = sampler.select(sentences)

# 4) Now get these new samples labeled and update your model!
~~~


## API overview

See [detailed API description here](./docs/api.md).


## Roadmap

See [a list of future work items here](./docs/roadmap.md).


## References

Ash, Jordan T., et al. "Deep batch active learning by diverse, uncertain gradient lower bounds." International Conference on Learning Representations. 2020.

Ash, Jordan T., et al. "Gone fishing: Neural active learning with fisher embeddings." Advances in Neural Information Processing Systems. 2021.

Saran, Akanksha, et al. "Streaming Active Learning with Deep Neural Networks." International Conference on Machine Learning. 2023.
