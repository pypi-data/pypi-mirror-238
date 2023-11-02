import logging
from typing import List

from guardrail.firewall.input_detectors.language import LanguageInput
from guardrail.firewall.output_detectors.base_detector import Detector

log = logging.getLogger(__name__)

class LanguageOutput(Detector):

    def __init__(self, valid_languages: List[str]):
        """
        Initializes the Language scanner with a list of valid languages.

        Parameters:
            valid_languages (List[str]): A list of valid language codes.
        """

        self._scanner = LanguageInput(valid_languages=valid_languages)

    def scan(self, prompt: str, output: str) -> (str, bool, float):
        return self._scanner.scan(output)