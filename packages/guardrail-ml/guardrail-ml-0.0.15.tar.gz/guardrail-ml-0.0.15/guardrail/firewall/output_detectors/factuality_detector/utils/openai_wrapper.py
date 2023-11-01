from __future__ import annotations

import os
import yaml
import ast
import pdb
import asyncio
from typing import Any, List
import os
import pathlib
import openai
import re
import asyncio
from guardrail.metrics.utils.keys import init_keys
from guardrail.tracker.openai import OpenAI

class OpenAIChat():
    def __init__(
            self,
            model_name='gpt-4-8k',
            max_tokens=2500,
            temperature=0,
            top_p=1,
            request_timeout=120,
    ):
        if 'gpt' not in model_name:
            openai.api_base = "http://localhost:8000/v1"
        else:
            #openai.api_base = "https://api.openai.com/v1"
            openai.api_key = os.environ.get("OPENAI_API_KEY", None)
            assert openai.api_key is not None, "Please set the OPENAI_API_KEY environment variable."
            assert openai.api_key !='', "Please set the OPENAI_API_KEY environment variable."

        self.config = {
            'model_name': model_name,
            'max_tokens': max_tokens,
            'temperature': temperature,
            'top_p': top_p,
            'request_timeout': request_timeout,
        }
        self.openai_gr = OpenAI(firewall=None)

    def extract_list_from_string(self, input_string):
        # pattern = r'\[.*\]'  
        # result = re.search(pattern, input_string)
        # if result:
        #     return result.group()
        # else:
        #     return None
        start_index = input_string.find('[')  
        end_index = input_string.rfind(']') 

        if start_index != -1 and end_index != -1 and start_index < end_index:
            return input_string[start_index:end_index + 1]
        else:
            return None
        
    def extract_dict_from_string(self, input_string):
        start_index = input_string.find('{')
        end_index = input_string.rfind('}')

        if start_index != -1 and end_index != -1 and start_index < end_index:
            return input_string[start_index:end_index + 1]
        else:
            return None
    
    def _boolean_fix(self, output):
        return output.replace("true", "True").replace("false", "False")

    def _type_check(self, output, expected_type):
        try:
            output_eval = ast.literal_eval(output)
            if not isinstance(output_eval, expected_type):
                return None
            return output_eval
        except:
            '''
            if(expected_type == List):
                valid_output = self.extract_list_from_string(output)
                output_eval = ast.literal_eval(valid_output)
                if not isinstance(output_eval, expected_type):
                    return None
                return output_eval
            elif(expected_type == dict):
                valid_output = self.extract_dict_from_string(output)
                output_eval = ast.literal_eval(valid_output)
                if not isinstance(output_eval, expected_type):
                    return None
                return output_eval
            '''
            return None

    async def dispatch_openai_requests(
        self,
        messages_list,
    ) -> list[str]:
        """Dispatches requests to OpenAI API asynchronously.
        
        Args:
            messages_list: List of messages to be sent to OpenAI ChatCompletion API.
        Returns:
            List of responses from OpenAI API.
        """
        async def _request_with_retry(messages, retry=3):
            for _ in range(retry):
                try:
                    response = self.openai_gr.run_chat_completion(
                        model=self.config['model_name'],
                        messages=messages,
                        max_tokens=self.config['max_tokens'],
                        temperature=self.config['temperature'],
                        top_p=self.config['top_p'],
                        request_timeout=self.config['request_timeout'],
                    )
                    return response
                except openai.error.RateLimitError:
                    print('Rate limit error, waiting for 40 second...')
                    await asyncio.sleep(40)
                except openai.error.APIError:
                    print('API error, waiting for 1 second...')
                    await asyncio.sleep(1)
                except openai.error.Timeout:
                    print('Timeout error, waiting for 1 second...')
                    await asyncio.sleep(1)
                except openai.error.ServiceUnavailableError:
                    print('Service unavailable error, waiting for 3 second...')
                    await asyncio.sleep(3)
                except openai.error.APIConnectionError:
                    print('API Connection error, waiting for 3 second...')
                    await asyncio.sleep(3)

            return None

        async_responses = [
            _request_with_retry(messages)
            for messages in messages_list
        ]

        return await asyncio.gather(*async_responses)
    
    async def async_run(self, messages_list, expected_type):
        retry = 1
        responses = [None for _ in range(len(messages_list))]
        messages_list_cur_index = [i for i in range(len(messages_list))]

        while retry > 0 and len(messages_list_cur_index) > 0:
            print(f'{retry} retry left...')
            messages_list_cur = [messages_list[i] for i in messages_list_cur_index]
            
            predictions = await self.dispatch_openai_requests(
                messages_list=messages_list_cur,
            )

            preds = [self._type_check(self._boolean_fix(prediction['choices'][0]['message']['content']), expected_type) if prediction is not None else None for prediction in predictions]

            finised_index = []
            for i, pred in enumerate(preds):
                if pred is not None:
                    responses[messages_list_cur_index[i]] = pred
                    finised_index.append(messages_list_cur_index[i])
            
            messages_list_cur_index = [i for i in messages_list_cur_index if i not in finised_index]
            
            retry -= 1
        
        return responses

class OpenAIEmbedWrapper():
    def __init__(self):
        init_keys()
        assert openai.api_key is not None, "Please set the OPENAI_API_KEY environment variable."
        assert openai.api_key != '', "Please set the OPENAI_API_KEY environment variable."

    async def create_embedding(self, text, retry=3):
        for _ in range(retry):
            try:
                response = await openai.Embedding.acreate(input=text, model="text-embedding-ada-002")
                return response
            except openai.error.RateLimitError:
                print('Rate limit error, waiting for 1 second...')
                await asyncio.sleep(1)
            except openai.error.APIError:
                print('API error, waiting for 1 second...')
                await asyncio.sleep(1)
            except openai.error.Timeout:
                print('Timeout error, waiting for 1 second...')
                await asyncio.sleep(1)
        return None

    async def process_batch(self, batch, retry=3):
        tasks = [self.create_embedding(text, retry=retry) for text in batch]
        return await asyncio.gather(*tasks)