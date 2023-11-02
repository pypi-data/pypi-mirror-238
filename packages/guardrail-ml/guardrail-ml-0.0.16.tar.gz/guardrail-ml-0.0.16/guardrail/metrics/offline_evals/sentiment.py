import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification


class Sentiment:
    def __init__(self, model_name="textattack/bert-base-uncased-imdb"):
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForSequenceClassification.from_pretrained(model_name)

    def evaluate(self, text, max_length=None):
        if max_length is None:
            # Use the default max_length of the model
            inputs = self.tokenizer(text, return_tensors="pt")
        else:
            # Set a custom max_length
            inputs = self.tokenizer(text, return_tensors="pt", max_length=max_length, truncation=True)

        outputs = self.model(**inputs)
        probabilities = torch.softmax(outputs.logits, dim=1)
        return probabilities[0, 1].item()
