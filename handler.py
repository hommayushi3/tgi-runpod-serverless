import os
import logging
import runpod
from text_generation import Client
from time import sleep

logging.basicConfig(level=os.getenv("LOG_LEVEL", "INFO"))

generator = None
default_settings = None
prompt_prefix = os.getenv("PROMPT_PREFIX", "")
prompt_suffix = os.getenv("PROMPT_SUFFIX", "")

max_wait = 60 * 3

def inference(event) -> str:
    logging.info(event)
    job_input = event["input"]
    prompt: str = prompt_prefix + job_input.pop("prompt") + prompt_suffix
    client = Client("http://localhost:80")

    output = ""
    for i in range(max_wait):
        try:
            output = client.generate(prompt, **job_input).generated_text
            break
        except Exception as e:
            logging.info(e)
            sleep(1)

    return output

runpod.serverless.start({"handler": inference})
