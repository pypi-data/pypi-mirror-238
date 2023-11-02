import os
import openai
from dotenv import load_dotenv, find_dotenv
from guardrail.client import set_env_vars
import os

class InvalidApiKeyError(Exception):
    pass

def load_api_key(env_var_name):
    """
    Load an API key from an environment variable.

    Parameters:
        env_var_name (str): The name of the environment variable containing the API key.

    Returns:
        str: The API key.
    """
    api_key = os.getenv(env_var_name)
    if not api_key:
        raise ValueError(f"{env_var_name} not found in environment variables.")
    return api_key

def init_openai_key():
    """
    Initialize the OpenAI API key from the environment variable.
    """
    openai_api_key = load_api_key("OPENAI_API_KEY")
    openai.api_key = openai_api_key

def init_guardrail_key(key=""):
    """
    Initialize the Guardrail API key from the environment variable.
    """
    if key == "":
        guardrail_api_key = load_api_key("GUARDRAIL_API_KEY")
        if guardrail_api_key == "":
            raise InvalidApiKeyError("Please enter a valid Guardrail API Key.")   
    else:
        guardrail_api_key = key
    set_env_vars({"GUARDRAIL_API_KEY": guardrail_api_key})

def init_perspective_key():
    """
    Initialize the Perspective API key from the environment variable.
    """
    perspective_api_key = load_api_key("PERSPECTIVE_API_KEY")

    set_env_vars({"PERSPECTIVE_API_KEY": perspective_api_key})

def init_keys(api_keys=None):
    """
    Initialize API keys for OpenAI and Guardrail.

    Parameters:
        api_keys (dict, optional): A dictionary containing API keys. If provided, it will set the environment variables.
    """
    if api_keys:
        set_env_vars(api_keys)
    init_guardrail_key()
    init_openai_key()