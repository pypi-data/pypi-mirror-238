"""
1. run_metrics
2. create_dataset 
3. init_logs 
"""

import logging
import sqlite3
from dotenv import set_key

from .metrics.offline_evals import Bias, Toxicity, Relevance, PromptInjection, Sentiment, Textstat

from .db import insert_log

def set_env_vars(file_path='.env', variables_dict={}):
    """
    Set environment variables programmatically in a .env file.

    Args:
        file_path (str): The path to the .env file.
        variables_dict (dict): A dictionary where keys are variable names and values are their corresponding values.
    """
    for variable, value in variables_dict.items():
        set_key(file_path, variable, value)

def run_simple_metrics(output, prompt, model_uri):
    # Initialize the Textstat class
    textstat = Textstat()

    # Configure logging
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger("Textstat")

    ts_eval_results = textstat.evaluate(output)

    for result_name in ts_eval_results:
        try:
            # Insert log into the database
            insert_log(model_uri, prompt, output, result_name, ts_eval_results[result_name])
        except Exception as e:
            logger.error(f"Error while inserting {result_name} into DB: {e}")

    return ts_eval_results



def run_metrics(output, prompt, model_uri):
    # Initialize the metrics classes
    textstat = Textstat()
    toxicity = Toxicity()
    relevance = Relevance()
    injection = PromptInjection()
    sentiment = Sentiment()
    bias = Bias()

    # Configure logging
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger("Textstat")

    results = {}
    ts_results = textstat.evaluate(output)
    sentiment_results = sentiment.evaluate(output)
    bias_results = bias.evaluate(output)

    if prompt:
        relevance_results = relevance.evaluate(output, prompt)
        injection_results = injection.evaluate(prompt)
        toxicity_results = toxicity.evaluate(output, prompt)

    results["text_quality"] = ts_results
    for result_name in ts_results:
        try:
            # Insert log into the database
            insert_log(
                model_uri,
                prompt,
                output,
                "tq_" + str(result_name),
                ts_results[result_name],
            )
        except Exception as e:
            logger.error(f"Error while inserting {result_name} into DB: {e}")

    insert_log(model_uri, prompt, output, "toxicity", toxicity_results)
    insert_log(model_uri, prompt, output, "sentiment", sentiment_results)
    insert_log(model_uri, prompt, output, "bias_label", bias_results[0]["label"])
    insert_log(model_uri, prompt, output, "bias_score", bias_results[0]["score"])

    results["toxicity"] = toxicity_results
    results["sentiment"] = sentiment_results
    results["bias"] = bias_results

    if relevance_results:
        results["relevance"] = relevance_results
        insert_log(model_uri, prompt, output, "relevance", relevance_results)
    if injection_results:
        results["prompt_injection"] = injection_results
        insert_log(model_uri, prompt, output, "prompt_injection", injection_results)
    return results


