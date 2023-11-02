import logging
import concurrent.futures
import spacy.cli
from typing import Dict, List, Tuple

from guardrail.metrics.utils.keys import init_keys, init_guardrail_key
from guardrail.firewall.input_detectors.base_detector import Detector as InputDetector
from guardrail.firewall.output_detectors.base_detector import Detector as OutputDetector

from guardrail.firewall.vault import Vault
from guardrail.firewall.input_detectors import Anonymize, Secrets, PromptInjections, DoSTokens, StopInputSubstrings, MalwareInputURL, HarmfulInput, TextQualityInput
from guardrail.firewall.output_detectors import Deanonymize, SensitivePII, StopOutputSubstrings, FactualityTool, FactualConsistency, MalwareOutputURL, HarmfulOutput, TextQualityOutput, Bias, Relevance

from guardrail.tracker.base_tracker import GuardrailBaseTracker

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)

model_name = "en_core_web_trf"

class Firewall(GuardrailBaseTracker):
    def __init__(self, foundation_model="gpt-3.5-turbo", no_defaults=False):
        init_keys()
        self.foundation_model = foundation_model
        self.vault = Vault()
        self.no_defaults = no_defaults
        if not self.no_defaults:
            spacy.cli.download(model_name)
            self.default_input_detectors =  [Anonymize(self.vault), Secrets(), PromptInjections(), DoSTokens(), StopInputSubstrings(), MalwareInputURL(), HarmfulInput(), TextQualityInput()]
            self.default_output_detectors = [SensitivePII(), Deanonymize(self.vault), StopOutputSubstrings(), FactualConsistency(), MalwareOutputURL(), HarmfulOutput(), TextQualityOutput(), Bias(), Relevance()]
        
        self.input_risk_scores = {}
        self.output_risk_scores = {}

    def clear_input_detectors(self):
        """Clear the list of input detectors."""
        self.default_input_detectors.clear()

    def clear_output_detectors(self):
        """Clear the list of output detectors."""
        self.default_output_detectors.clear()

    def add_to_input_detectors(self, detector: InputDetector):
        """
        Add an input detector to the list of input detectors.

        Args:
            detector (InputDetector): An instance of an input detector class.
        """
        self.default_input_detectors.append(detector)

    def add_to_output_detectors(self, detector: OutputDetector):
        """
        Add an output detector to the list of output detectors.

        Args:
            detector (OutputDetector): An instance of an output detector class.
        """
        self.default_output_detectors.append(detector)
    
    def print_detectors(self):
        print("Input Detectors: ", self.default_input_detectors)
        print("Output Detectors: ", self.default_output_detectors)

    def scan_input(self,
                   prompt: str,
                   detectors: List[InputDetector] = None,
                   ) -> Tuple[str, Dict[str, bool], Dict[str, float]]:
        """
        Scans a given prompt using the provided detectors or default detectors.

        Args:
            detectors (List[InputDetector], optional): A list of detector objects. Each detector should be an instance of a class that inherits from `Detector`. Defaults to None.
            prompt (str, optional): The input prompt string to be scanned. Defaults to an empty string.

        Returns:
            Tuple[str, Dict[str, bool], Dict[str, float]]: A tuple containing:
                - The processed prompt string after applying all detectors.
                - A dictionary mapping detector names to boolean values indicating whether the input prompt is valid according to each detector.
                - A dictionary mapping detector names to float values of risk scores, where 0 is no risk, and 1 is high risk.
        """

        sanitized_prompt = prompt
        results_valid = {}
        results_score = {}

        if detectors is None:
            detectors = self.default_input_detectors

        if len(detectors) == 0 or prompt.strip() == "":
            return sanitized_prompt, results_valid, results_score

        # Create a ThreadPoolExecutor to parallelize detector execution
        with concurrent.futures.ThreadPoolExecutor() as executor:
            # Submit detector jobs and collect futures
            futures = {executor.submit(detector.scan, sanitized_prompt): detector for detector in detectors}

            # Collect results from completed futures
            for future in concurrent.futures.as_completed(futures):
                detector = futures[future]
                sanitized_prompt, is_valid, risk_score = future.result()
                results_valid[type(detector).__name__] = is_valid
                results_score[type(detector).__name__] = risk_score
            
            self.input_risk_scores = results_score

        return sanitized_prompt, results_valid, results_score
        
    def scan_output(self,
                    prompt: str,
                    output: str,
                    detectors: List[OutputDetector] = None,
                    ) -> Tuple[str, Dict[str, bool], Dict[str, float]]:
        """
        Scans a given output of a large language model using the provided detectors or default detectors.

        Args:
            detectors (List[OutputDectector], optional): A list of detector objects. Each detector should be an instance of a class that inherits from `Detector`. Defaults to None.
            prompt (str, optional): The input prompt string that produced the output. Defaults to an empty string.
            output (str, optional): The output string to be scanned. Defaults to an empty string.

        Returns:
            Tuple[str, Dict[str, bool], Dict[str, float]]: A tuple containing:
                - The processed output string after applying all detectors.
                - A dictionary mapping detector names to boolean values indicating whether the output is valid according to each detector.
                - A dictionary mapping detector names to float values of risk scores, where 0 is no risk, and 1 is high risk.
        """

        sanitized_output = output
        results_valid: Dict[str, bool] = {}
        results_score: Dict[str, float] = {}

        print("OUTPUT detectors == ", detectors)
        
        if not self.no_defaults and detectors is None:
            log.error("ERROR: no detectors passed to Firewall")
            return sanitized_output, results_valid, results_score
        elif detectors is not None:
            detectors = detectors
        else:
            detectors = self.default_output_detectors

        if not output.strip():
            log.error("ERROR: no output passed to Firewall")
            return sanitized_output, results_valid, results_score

        # Create a ThreadPoolExecutor to parallelize detector execution
        with concurrent.futures.ThreadPoolExecutor() as executor:
            # Submit detector jobs and collect futures
            futures = {executor.submit(detector.scan, prompt, sanitized_output): detector for detector in detectors}
                            
            # Collect results from completed futures
            for future in concurrent.futures.as_completed(futures):
                detector = futures[future]
                sanitized_output, is_valid, risk_score = future.result()
                results_valid[type(detector).__name__] = is_valid
                results_score[type(detector).__name__] = risk_score
            
            self.output_risk_scores = results_score
            # Send to backend API
            self.run_eval_store_logs_firewall(prompt, output, self.input_risk_scores, self.output_risk_scores)

        return sanitized_output, results_valid, results_score
