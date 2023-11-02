import time
from typing import Any, Dict, List

from langchain.chat_models import ChatOpenAI
from langchain.schema import LLMResult, HumanMessage
from langchain.callbacks.base import AsyncCallbackHandler, BaseCallbackHandler
from guardrail.tracker.base_tracker import GuardrailBaseTracker

class GuardrailCallbackHandler(AsyncCallbackHandler):
    """Async callback handler that can be used to handle callbacks from langchain."""

    def __init__(self, firewall):
        super().__init__()
        self.prompts = []  # Initialize an empty list to store prompts
        self.firewall = firewall
        self.base_tracker = GuardrailBaseTracker()

    async def on_llm_start(
        self, serialized: Dict[str, Any], prompts: List[str], **kwargs: Any
    ) -> None:
        """Run when chain starts running."""
        print("Guardrail is tracking...")
        print(prompts)

        # Store prompts in the instance variable
        prompts = prompts[-1]

        # Record the start time
        self.start_time = time.time()

        # Run firewall
        self.firewall.scan_input(prompts)

    async def on_llm_end(self, response: LLMResult, **kwargs: Any) -> None:
        """Run when chain ends running."""
        print("LLM chain is ending...")
        print(response)
        self.firewall.scan_output(response)

        # Calculate the total time elapsed
        end_time = time.time()
        total_time = end_time - self.start_time
        print(f"Total time elapsed: {total_time} seconds")
