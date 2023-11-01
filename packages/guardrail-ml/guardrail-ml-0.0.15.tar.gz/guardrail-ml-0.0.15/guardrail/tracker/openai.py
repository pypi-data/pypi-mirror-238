import time
import json
import requests
import openai
from threading import Thread

from guardrail.metrics.utils.keys import init_keys, load_api_key
from guardrail.env_config import guardrail_env_config
from guardrail.metrics.utils.flatten_metrics import flatten_json
from guardrail.metrics.offline_evals.offline_metrics import OfflineMetricsEvaluator
from guardrail.tracker.base_tracker import GuardrailBaseTracker

class OpenAI(GuardrailBaseTracker):
    def __init__(self, firewall, llm_model="gpt-3.5-turbo", api_keys={}):
        init_keys()
        self.llm_model = llm_model
        self.offline_metrics = OfflineMetricsEvaluator()
        self.firewall = firewall

    def create_completion(self, engine, prompt, gr_tags=None, **kwargs):
        kwargs['engine'] = engine
        kwargs['prompt'] = prompt
        if gr_tags:
            kwargs['gr_tags'] = gr_tags
        result = openai.Completion.create(**kwargs)        

    def create_chat_completion(self, model, messages, **kwargs):
        kwargs['model'] = model
        kwargs['messages'] = messages

        start_time = time.time()
        openai_response = self._chat_completion_request(**kwargs)
        
        prompt = self.get_latest_user_prompt(messages)
        chatbot_response = openai_response["choices"][0]["message"]["content"]

        end_time = time.time()
        total_time = end_time - start_time
        print(f"ChatCompletion executed in {total_time:.4f} seconds")

        return openai_response, chatbot_response
     
    def get_latest_user_prompt(self, messages):
        for message in reversed(messages):
            if message["role"] == "user":
                return message["content"]
        return None

    def run_chat_completion(self, 
                            messages, 
                            model="gpt-3.5-turbo", 
                            temperature=0, 
                            max_tokens=256, 
                            **kwargs):
        if isinstance(messages, str):
            messages = [{'role': 'user', 'content': messages}]
        
        start_time = time.time()

        prompt = messages[-1]['content']

        if self.firewall == None:
            openai_response, chatbot_response = self.create_chat_completion(
                model=model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens,
                **kwargs
            )
        else:
            sanitized_prompt, input_valid_results, input_risk_score = self.firewall.scan_input(prompt)
            print("Prompt Valid Results: ", input_valid_results)
            openai_response, chatbot_response = self.create_chat_completion(
                model=model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens,
                **kwargs
            )

            sanitized_response, output_valid_results, output_risk_score = self.firewall.scan_output(
                sanitized_prompt, chatbot_response
            )
            print("Output Valid Results: ", output_valid_results)

        end_time = time.time()
        total_time = end_time - start_time

        # Start storing logs in the background
        # eval_log_thread = Thread(target=self.run_eval_store_logs, args=(prompt, chatbot_response, openai_response["usage"], total_time, input_risk_score, output_risk_score))
        # eval_log_thread.start()

        # eval_log_thread.join()
        print(f"Total time executed in {total_time:.4f} seconds")

        if self.firewall == None:
            self.run_eval_store_logs(prompt, chatbot_response, openai_response["usage"], total_time, {}, {})
            return openai_response
        else:
            self.run_eval_store_logs(prompt, chatbot_response, openai_response["usage"], total_time, input_risk_score, output_risk_score)
            return sanitized_response, input_risk_score, output_risk_score

    def run_chat_completion_entry(self, user_message_content, model="gpt-3.5-turbo", temperature=0, max_tokens=256, **kwargs):
        self.run_chat_completion(user_message_content, model, temperature, max_tokens, **kwargs)

    def _chat_completion_request(self, **kwargs):
        return openai.ChatCompletion.create(**kwargs)
