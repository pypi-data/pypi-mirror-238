import unittest


class TestActiveModel(unittest.TestCase):
    def test_get_active_model(self):
        from active_learn import get_active_model
        from transformers import AutoModelForSequenceClassification, AutoTokenizer

        model_name = "gpt2"
        num_labels = 5

        model = AutoModelForSequenceClassification.from_pretrained(
            model_name,
            num_labels=num_labels,
            problem_type="multi_label_classification",
        )
        model.config.pad_token_id = model.config.eos_token_id
        self.assertFalse(hasattr(model, "get_embedding_dim"))
        self.assertFalse(hasattr(model, "get_outputs_and_embeddings"))

        model = get_active_model(model)
        self.assertTrue(hasattr(model, "get_embedding_dim"))
        self.assertTrue(hasattr(model, "get_outputs_and_embeddings"))
        self.assertEqual(model.get_embedding_dim(), 768)

        tokenizer = AutoTokenizer.from_pretrained(model_name)
        tokenizer.pad_token_id = model.config.pad_token_id

        example_sentences = [
            "This active learning tool is awesome!",
            "Less labeling data is needed using this tool.",
            "It can also increase the accuracy.",
        ]
        tokenized = tokenizer(example_sentences, padding=True)
        outputs, embeddings = model.get_outputs_and_embeddings(tokenized)
        self.assertEqual(len(outputs), len(example_sentences))
        self.assertEqual(len(outputs[0]), num_labels)
        self.assertEqual(len(embeddings), len(example_sentences))
        self.assertEqual(len(embeddings[0]), model.get_embedding_dim())

    def test_init_active_sampler_with_pretrained_model(self):
        from active_learn import ActiveSampler, get_active_model
        from transformers import AutoModelForSequenceClassification

        model = AutoModelForSequenceClassification.from_pretrained(
            "gpt2",
            num_labels=10,
            problem_type="multi_label_classification",
        )

        sampler_initialized = False
        try:
            sampler = ActiveSampler("classification", model, 1000)
            sampler_initialized = True
        except Exception:
            pass
        self.assertFalse(sampler_initialized)

        model = get_active_model(model)
        try:
            sampler = ActiveSampler("classification", model, 1000)
            sampler_initialized = True
        except Exception:
            pass
        self.assertTrue(sampler_initialized)
        self.assertTrue(hasattr(sampler, "select"))


if __name__ == "__main__":
    unittest.main()
