import yaml
from .openai_wrapper import OpenAIChat
import os
import pathlib

class pipeline():
    def __init__(self, domain, llm_model="gpt-3.5-turbo"):
        #if foundation_model == 'gpt-3.5-turbo' or foundation_model == 'gpt-4':
        self.company = 'openai'
        self.chat = OpenAIChat(model_name=llm_model)

        self.prompts_path = os.path.join(os.path.dirname(pathlib.Path(__file__)), "../prompts/")
        
        with open(os.path.join(self.prompts_path, "self_check.yaml"), 'r') as file:
            data = yaml.load(file, Loader=yaml.FullLoader)
        self.self_check_prompt = data[domain]