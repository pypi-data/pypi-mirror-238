import logging
import os
import re
import json
from typing import List, Optional

from guardrail.firewall.input_detectors.stop_input_substrings import allowed_match_type 
from guardrail.firewall.output_detectors.base_detector import Detector

log = logging.getLogger(__name__)
stop_file_path = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "..",
    "patterns",
    "output_stop_substrings.json",
)

class StopOutputSubstrings(Detector):
    """
    A text detector that checks and filters out banned substrings from generated text output.

    This class provides the functionality to filter substrings in two different ways: as 'str' or as 'word'.
    - 'str' filters out substrings found anywhere in the text.
    - 'word' filters out substrings found as whole words.
    """

    def __init__(
        self,
        match_type: str = "str",
        case_sensitive: bool = False,
        substrings: Optional[List[str]] = None,
    ):
        """
        Initializes FilterSubstrings with a match type, case sensitivity option, and a list of substrings.

        Parameters:
            match_type (str): The type of substring matching. Can be either 'str' or 'word'. Default is 'str'.
            case_sensitive (bool): Determines whether the substring matching is case sensitive. Default is False.
            substrings (Optional[List[str]]): The list of substrings to be filtered out from the text. Default is None.

        Raises:
            ValueError: If no substrings are provided or match_type is not 'str' or 'word'.
        """

        if match_type not in allowed_match_type:
            raise ValueError(f"This match_type is not recognized. Allowed: {allowed_match_type}")
        
        # Load default substrings
        default_substrings = self.load_default_substrings()

        if substrings:
            log.info("Using user-provided substrings in addition to default patterns.")
            self._substrings = default_substrings + substrings
        else:
            log.warning("Using default patterns...")
            self._substrings = default_substrings
        
        self._match_type = match_type  # str or word
        self._case_sensitive = case_sensitive
    
    def load_default_substrings(self) -> List[str]:
        """
        Load default substrings from a JSON file.

        Returns:
            List[str]: The default list of substrings.
        """
        default_substrings = []

        try:
            with open(stop_file_path, "r") as stop_file:
                data = json.load(stop_file)
                for key in data:
                    default_substrings.extend(data[key])
            return default_substrings
        except (FileNotFoundError, json.JSONDecodeError):
            log.warning("Failed to load default substrings. Using an empty list.")
            return []

    def scan(self, prompt:str, output: str) -> (str, bool, float):
        filtered_output = output
        matched_substrings = []
        for s in self._substrings:
            if self._case_sensitive:
                s, filtered_output = s.lower(), filtered_output.lower()

            if self._match_type == "str":
                filtered_output = filtered_output.replace(s, "")
                if s in output:
                    matched_substrings.append(s)
            elif self._match_type == "word":
                pattern = r"\b" + re.escape(s) + r"\b"
                filtered_output = re.sub(pattern, "", filtered_output)
                if re.search(pattern, output):
                    matched_substrings.append(s)

        if matched_substrings:
            log.warning(f"Filtered out the following banned substrings: {matched_substrings}")
            return filtered_output, False, 1.0

        log.debug("No banned substrings found")
        return filtered_output, True, 0.0
