import logging
from transformers import AutoModelForSequenceClassification, AutoTokenizer, TextClassificationPipeline
from guardrail.firewall.util import device
from guardrail.firewall.input_detectors.base_detector import Detector

_model_path_1 = "JasperLS/deberta-v3-base-injection"
_model_path_2 = "hubert233/GPTFuzz"
log = logging.getLogger(__name__)

class PromptInjections(Detector):

    def __init__(self, threshold: float = 0.75):
        model_1 = AutoModelForSequenceClassification.from_pretrained(_model_path_1)
        tokenizer_1 = AutoTokenizer.from_pretrained(_model_path_1)
        model_2 = AutoModelForSequenceClassification.from_pretrained(_model_path_2)
        tokenizer_2 = AutoTokenizer.from_pretrained(_model_path_2)
        
        self._threshold = threshold
        self._text_classification_pipeline_1 = TextClassificationPipeline(
            model=model_1,
            tokenizer=tokenizer_1,
            device=device,
        )
        self._text_classification_pipeline_2 = TextClassificationPipeline(
            model=model_2,
            tokenizer=tokenizer_2,
            device=device,
        )
        log.debug(f"Initialized models: {_model_path_1}, {_model_path_2} on device {device}")

    def scan(self, prompt: str) -> (str, bool, float):
        if prompt.strip() == "":
            return prompt, True, 0.0

        result_1 = self._text_classification_pipeline_1(
            prompt, truncation=True, max_length=self._text_classification_pipeline_1.tokenizer.model_max_length
        )
        result_2 = self._text_classification_pipeline_2(
            prompt, truncation=True, max_length=self._text_classification_pipeline_2.tokenizer.model_max_length
        )
        
        injection_score_1 = round(
            result_1[0]["score"] if result_1[0]["label"] == "INJECTION" else 1 - result_1[0]["score"], 2
        )
        injection_score_2 = round(
            result_2[0]["score"] if result_2[0]["label"] == "INJECTION" else 1 - result_2[0]["score"], 2
        )

        if injection_score_1 > self._threshold or injection_score_2 > self._threshold:
            log.warning(
                f"Detected prompt injection with scores: Model 1 - {injection_score_1}, Model 2 - {injection_score_2}, threshold: {self._threshold}"
            )
            return prompt, False, max(injection_score_1, injection_score_2)

        log.debug(
            f"No prompt injection detected (Model 1 score: {injection_score_1}, Model 2 score: {injection_score_2}, threshold: {self._threshold})"
        )
        return prompt, True, 0.0
