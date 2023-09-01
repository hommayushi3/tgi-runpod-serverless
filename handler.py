import runpod
import os
from text_generation import Client
from copy import copy
import inspect
import warnings
import asyncio
import time
from json import loads

class RequestCounter:
    """
    A concurrency controller that keeps track of the number of concurrent requests.
    """
    def __init__(self):
        self.counter = 0
        self.lock = asyncio.Lock()

    async def increment(self):
        async with self.lock:
            self.counter += 1

    async def decrement(self):
        async with self.lock:
            self.counter -= 1

request_counter = RequestCounter()

def concurrency_controller() -> bool:
    return request_counter.counter > 0


# Create the text-generation-inference asynchronous client
client = Client(base_url="http://localhost:80")

# Get valid arguments for generate and generate_stream
valid_non_stream_arguments = inspect.getfullargspec(client.generate).args
valid_stream_arguments = inspect.getfullargspec(client.generate_stream).args

# Get default generate parameters from environment variable
DEFAULT_GENERATE_PARAMS = loads(os.getenv("DEFAULT_GENERATE_PARAMS", "{}"))

# Verify that the default generate parameters are valid
temp_default_generate_params = copy(DEFAULT_GENERATE_PARAMS)
for key in DEFAULT_GENERATE_PARAMS.keys():
    if key not in valid_non_stream_arguments and key not in valid_stream_arguments:
        warnings.warn(f"Warning: Invalid generate parameter: {key} passed in DEFAULT_GENERATE_PARAMS. Removing from DEFAULT_GENERATE_PARAMS.")
        raise ValueError(
            f"Invalid generate parameter: {key}. Valid parameters are: {valid_non_stream_arguments + valid_stream_arguments}"
        )
    temp_default_generate_params.pop(key)
DEFAULT_GENERATE_PARAMS = temp_default_generate_params


def handler(job):
    '''
    This is the handler function that will be called by the serverless worker.
    '''
    request_counter.increment()
    print(f"Starting request {job}, active requests: {request_counter.counter}")
    start = time.time()

    # Get job input
    job_input = job['input']
    prompt = job_input['prompt']

    # Set Generate Params
    generate_params = copy(DEFAULT_GENERATE_PARAMS)
    generate_params.update(job_input.pop('generate_params', {}))

    # Set Stream Option
    stream = job_input.pop('stream', False)

    # Print the prompt and generate_params
    print("**** PROMPT ****")
    print(prompt)
    print("**** GENERATE PARAMS ****")
    print(generate_params)
    print(f"**** STREAMING: {stream} ****")

    # Send request to Text Generation Inference Server and yield results
    if stream:
        for _ in range(20):
            try:
                results_generator = client.generate_stream(prompt, **generate_params)
                for response in results_generator:
                    if not response.token.special:
                        yield {"text": response.token.text}
            except Exception:
                time.sleep(10)

    else:
        for _ in range(20):
            try:
                result = client.generate(prompt, **generate_params)
                break
            except:
                time.sleep(10)
        yield {"text": result.generated_text}

    # Decrement the request counter
    request_counter.decrement()
    print(f"Finished request in {int(time.time() - start)} seconds, active requests: {request_counter.counter}")


# Start the serverless worker
print("Starting the TGI serverless worker with streaming enabled.")
runpod.serverless.start(
    {"handler": handler, "concurrency_controller": concurrency_controller, "return_aggregate_stream": True}
)
