# Active Learning Demo

## Basic Usage

~~~ python
from active_learn import ActiveSampler

sampler = ActiveSampler("classification", model, budget=1000)  # See detailed usage in API doc
chosen_indices = sampler.select(X_candidates)
~~~

## Run Demo

<!-- TODO: Update docs -->

1. Build & install `active_learn` package and other `requirements.txt`.
2. Run `demo.py` with and without `--random_sample` to see the difference.

<!-- TODO: Redraw chart with swapped axises. -->

![demo](./custom_model/wandb_chart.png)
