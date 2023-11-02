import logging
import asyncio
import copy
import json 
from typing import Dict, List, Tuple

from .pipeline import knowledge_qa_pipeline
from guardrail.metrics.utils.keys import init_keys

from guardrail.firewall.output_detectors.base_detector import Detector

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)

class FactualityTool(Detector):
    def __init__(self, 
                 foundation_model="gpt-3.5-turbo", 
                 search_type="online",
                 category="kbqa",
                 threshold=0.5):
        init_keys()
        self.foundation_model = foundation_model
        self.pipelines = {
                            "kbqa_online": knowledge_qa_pipeline(
                                foundation_model, 10, "online"
                            )
                            }
        self.search_type = search_type
        self.category=category
        self.threshold = threshold
        
    def scan(self, prompt: str, output: str) -> Tuple[str, bool, float]:
        inputs = [
            {
                "prompt": prompt,
                "response": output,
                "category": self.category,
                "search_type": self.search_type
            },
        ]
        factuality_results = self.run(inputs)

        # Prettify the JSON response
        prettified_response = json.dumps(factuality_results, indent=4)
        print(prettified_response)

        log.debug(factuality_results)

        corrected_response = self.get_corrected_factual_response(factuality_results)
        risk_score_claim = 1 - factuality_results["average_claim_level_factuality"]
        risk_score_response = 1 - factuality_results["average_response_level_factuality"]

        if risk_score_claim > self.threshold or risk_score_response > self.threshold:
            return corrected_response, False, max(risk_score_claim, risk_score_response)
        return corrected_response, True, max(risk_score_claim, risk_score_response)
    
    def get_corrected_factual_response(self, factuality_results):
        corrected_response = ""
        for detail_info in factuality_results["detailed_information"]:
            response = detail_info["response"]
            for claim, claim_factuality in zip(detail_info["claims"], detail_info["claim_level_factuality"]):
                if not claim_factuality["factuality"]:
                    # Replace false claims with corrections in the response
                    claim_text = claim["claim"]
                    correction_text = claim_factuality["correction"]
                    response = response.replace(claim_text, correction_text)
            corrected_response = response
        return corrected_response
    
    def run(self, inputs):
        outputs = copy.deepcopy(inputs)
        batches = []
        current_category = inputs[0]['category']
        current_search_type = inputs[0].get('search_type', None)
        current_data_link = inputs[0].get('data_link', None)
        current_embedding_link = inputs[0].get('embedding_link', None)
        current_batch = []

        for input in inputs:
            if (input['category'] == current_category != 'kbqa') \
                or (input['category'] == current_category == 'kbqa' and input.get('search_type', None) == current_search_type == "online") \
                    or (input['category'] == current_category == 'kbqa' and input.get('search_type', None) == current_search_type == "local"\
                        and input.get('data_link', None)==current_data_link and input.get('embedding_link', None)==current_embedding_link):
                current_batch.append(input)
            else:
                batches.append(current_batch)
                current_batch = [input]
                current_category = input['category']
                current_search_type = input.get('search_type', None)
                current_data_link = input.get('data_link', None)
                current_embedding_link = input.get('embedding_link', None)

        batches.append(current_batch)  # append the last batch

        index = 0
        for batch in batches:
            if not batch: continue
            category = batch[0]['category']
            search_type = batch[0].get('search_type', None)
            if category == 'code':
                batch_results = asyncio.run(
                    self.pipelines[category].run_with_tool_api_call(
                        [sample['prompt'] for sample in batch],
                        [sample['response'] for sample in batch],
                        [sample['entry_point'] for sample in batch]
                    )
                )
            elif category == 'kbqa':
                if search_type is None or search_type == "online":
                    batch_results = asyncio.run(
                        self.pipelines[category+"_online"].run_with_tool_api_call(
                            [sample['prompt'] for sample in batch],
                            [sample['response'] for sample in batch],
                        )
                    )
                else:
                    batch_results = asyncio.run(
                        knowledge_qa_pipeline(
                            self.foundation_model,2,"local",batch[0].get("data_link"),batch[0].get("embedding_link")
                        ).run_with_tool_api_call(
                            [sample['prompt'] for sample in batch],
                            [sample['response'] for sample in batch],
                        )
                    )
            else:
                batch_results = asyncio.run(
                    self.pipelines[category].run_with_tool_api_call(
                        [sample['prompt'] for sample in batch],
                        [sample['response'] for sample in batch]
                    )
                )
            for result in batch_results:
                outputs[index].update(result)
                index += 1

        # calculate average response_level_factuality
        total_response_factuality = sum(output['response_level_factuality'] == True for output in outputs)
        avg_response_level_factuality = total_response_factuality / len(outputs)

        # calculate average claim_level_factuality
        num_claims = 0
        total_claim_factuality = 0
        for output in outputs:
            num_claims += len(output['claim_level_factuality'])
            if output['category'] == 'kbqa':
                total_claim_factuality += sum(claim['factuality'] == True for claim in output['claim_level_factuality'])
            elif output['category'] == 'code':
                total_claim_factuality += (output['claim_level_factuality'] == True)
            elif output['category'] == 'math':
                total_claim_factuality += sum(claim_factuality == True for claim_factuality in output['claim_level_factuality'])
            elif output['category'] == 'scientific':
                total_claim_factuality += sum(claim['factuality'] == True for claim in output['claim_level_factuality'])

        avg_claim_level_factuality = total_claim_factuality / num_claims

        return {"average_claim_level_factuality": avg_claim_level_factuality, "average_response_level_factuality": avg_response_level_factuality, "detailed_information": outputs}

    async def run_for_plugin(self, inputs):
        outputs = copy.deepcopy(inputs)

        batches = []
        current_category = inputs[0]['category']
        current_batch = []

        for input in inputs:
            if input['category'] == current_category:
                current_batch.append(input)
            else:
                batches.append(current_batch)
                current_batch = [input]
                current_category = input['category']

        batches.append(current_batch)  # append the last batch

        index = 0
        for batch in batches:
            category = batch[0]['category']
            if category == 'code':
                batch_results = await self.pipelines[category].run_with_tool_api_call(
                    [sample['prompt'] for sample in batch],
                    [sample['response'] for sample in batch],
                    [sample['entry_point'] for sample in batch],
                )
            else:
                batch_results = await self.pipelines[category].run_with_tool_api_call(
                    [sample['prompt'] for sample in batch],
                    [sample['response'] for sample in batch],
                )
            for result in batch_results:
                outputs[index].update(result)
                index += 1

        return outputs
    
   