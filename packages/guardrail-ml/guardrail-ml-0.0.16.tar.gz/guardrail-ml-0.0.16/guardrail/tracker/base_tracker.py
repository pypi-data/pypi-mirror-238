import time
import json
import requests
import openai
from threading import Thread

from guardrail.metrics.utils.keys import init_keys, load_api_key
from guardrail.env_config import guardrail_env_config
from guardrail.metrics.utils.flatten_metrics import flatten_json
from guardrail.metrics.offline_evals.offline_metrics import OfflineMetricsEvaluator

class GuardrailBaseTracker:
    def __init__(self):
        self.offline_metrics = OfflineMetricsEvaluator()
    
    def flatten_evaluations(self, evaluations, parent_key='', separator='_'):
        """
        Flatten the "evaluations" dictionary.

        Parameters:
        - evaluations (dict): The "evaluations" dictionary to flatten.
        - parent_key (str): The parent key used for recursion. Leave empty for the initial call.
        - separator (str): The separator to use between flattened keys.

        Returns:
        - dict: The flattened "evaluations" dictionary.
        """
        flattened = {}
        risk_flag = "pass"
        failure_reasons = []  # Initialize an empty list for failure reasons
        for key, value in evaluations.items():
            new_key = f"{parent_key}{separator}{key}" if parent_key else key
            if isinstance(value, dict):
                result = self.flatten_evaluations(value, new_key, separator)
                flattened.update(result)
                if result.get("risk_status") == "fail":
                    failure_reasons.append(result.get("failure_reason"))
            else:
                flattened[new_key] = value
                try:
                    float_value = float(value)
                    if key == "Anonymize" and float_value >= 0.75:
                        risk_flag = "mitigated"
                    elif 0.75 <= float_value <= 1.0:
                        risk_flag = "fail"
                        # Add the triggering key to the failure reasons list
                        failure_reasons.append(new_key)
                except ValueError:
                    # Handle the case where the string is not a valid float
                    pass
        flattened["risk_status"] = risk_flag
        if risk_flag == "fail":
            flattened["failure_reason"] = " ".join(failure_reasons)
        return flattened
    
    def convert_numbers_to_strings(self, d):
        new_dict = {}
        for key, value in d.items():
            if isinstance(value, dict):
                # If the value is another dictionary, recursively call the function
                new_dict[key] = self.convert_numbers_to_strings(value)
            elif isinstance(value, (int, float)):
                # If the value is an int or float, convert it to a string
                new_dict[key] = str(value)
            else:
                new_dict[key] = value  # Keep other types unchanged
        return new_dict
    
    def run_eval_store_logs(self, prompt, output, openai_usage, total_time, input_risk_score, output_risk_score, model_name="gpt-3.5-turbo"):
        # Simulate storing logs
        print("prompt: ", prompt)
        print("output: ", output)
        cost = self.calculate_openai_cost(openai_usage, model_name)

        promptEvaluations = self.flatten_evaluations(self.convert_numbers_to_strings(input_risk_score))
        outputEvaluations = self.flatten_evaluations(self.convert_numbers_to_strings(output_risk_score))

        total_tokens = openai_usage["total_tokens"]

        api_key = guardrail_env_config.guardrail_api_key
        if api_key == "" or api_key == None:
            api_key = load_api_key("GUARDRAIL_API_KEY")
    
        api_url = "https://guardrail-api-sknmgpkina-uc.a.run.app/v1/create_evaluation_log"
        headers = {
            'Content-Type': 'application/json',  # Set Content-Type to indicate JSON data
            'Authorization': f'Bearer {api_key}'  # Replace api_key with your actual token
        }

        data = {
            "prompt": prompt,
            "output": output,
            "cost": str(cost),
            "llmToken": str(total_tokens),
            "latency": str(total_time),
            "promptEvaluations": promptEvaluations,
            "outputEvaluations": outputEvaluations,
        }

        response = requests.post(api_url, headers=headers, json=data)
        print(response.status_code)

        if response.status_code == 200:
            print("Stored logs successfully: ", response)
            print(response.json())
            return response.json()
        elif response.status_code == 403 or response.status_code >= 400:
            # Capture 403 errors and any 400+ errors
            print("Error Status Code:", response.status_code)
            print("Response Content:", response.content)
            print("Response Headers:", response.headers)
            return None
        else:
            # Handle other status codes as needed
            print("Unhandled Status Code:", response.status_code)
            return None
        
    def run_eval_store_logs_firewall(self, prompt, output, input_risk_score, output_risk_score, model_name="gpt-3.5-turbo"):
        # Simulate storing logs
        print("prompt: ", prompt)
        print("output: ", output)

        promptEvaluations = self.flatten_evaluations(self.convert_numbers_to_strings(input_risk_score))
        outputEvaluations = self.flatten_evaluations(self.convert_numbers_to_strings(output_risk_score))

        api_key = guardrail_env_config.guardrail_api_key
        if api_key == "" or api_key == None:
            api_key = load_api_key("GUARDRAIL_API_KEY")
    
        api_url = "https://guardrail-api-sknmgpkina-uc.a.run.app/v1/create_evaluation_log"
        headers = {
            'Content-Type': 'application/json',  # Set Content-Type to indicate JSON data
            'Authorization': f'Bearer {api_key}'  # Replace api_key with your actual token
        }

        data = {
            "prompt": prompt,
            "output": output,
            "cost": "NA",
            "llmToken": "NA",
            "latency": "NA",
            "promptEvaluations": promptEvaluations,
            "outputEvaluations": outputEvaluations,
        }

        response = requests.post(api_url, headers=headers, json=data)
        print(response.status_code)

        if response.status_code == 200:
            print("Stored logs successfully: ", response)
            print(response.json())
            return response.json()
        elif response.status_code == 403 or response.status_code >= 400:
            # Capture 403 errors and any 400+ errors
            print("Error Status Code:", response.status_code)
            print("Response Content:", response.content)
            print("Response Headers:", response.headers)
            return None
        else:
            # Handle other status codes as needed
            print("Unhandled Status Code:", response.status_code)
            return None

    def _run_offline_metrics(self, prompt, response):
        results = self.offline_metrics.evaluate_metrics(response, prompt)
        results = flatten_json(results)
        print(results)
        return results

    def calculate_openai_cost(self, usage, model="gpt-3.5-turbo"):
        pricing = {
            'gpt-3.5-turbo': {
                'prompt': 0.0015,
                'completion': 0.002,
            },
            'gpt-3.5-turbo-16k': {
                'prompt': 0.003,
                'completion': 0.004,
            },
            'gpt-4-8k': {
                'prompt': 0.03,
                'completion': 0.06,
            },
            'gpt-4-32k': {
                'prompt': 0.06,
                'completion': 0.12,
            },
            'text-embedding-ada-002-v2': {
                'prompt': 0.0001,
                'completion': 0.0001,
            }
        }

        try:
            model_pricing = pricing[model]
        except KeyError:
            raise ValueError("Invalid model specified")

        prompt_cost = usage['prompt_tokens'] * model_pricing['prompt'] / 1000
        completion_cost = usage['completion_tokens'] * model_pricing['completion'] / 1000

        total_cost = prompt_cost + completion_cost
        print(f"\nTokens used:  {usage['prompt_tokens']:,} prompt + {usage['completion_tokens']:,} completion = {usage['total_tokens']:,} tokens")
        print(f"Total cost for {model}: ${total_cost:.6f}\n")

        return total_cost