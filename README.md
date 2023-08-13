# tgi-runpod-serverless
Runs HuggingFace's text-generation-inference on Runpod Serverless.

Modeled off of [worker-vllm](https://github.com/runpod-workers/worker-vllm) repo.

<details>
    <summary>Inference Call from Client</summary>
```py
import os
import requests
from time import sleep
import logging

os.environ["RUNPOD_AI_API_KEY"] = ".................................."

endpoint_id = "..........."
URI = f"https://api.runpod.ai/v2/{endpoint_id}/run"

def run(prompt):
    request = {
        'prompt': prompt,
        'temperature': 0.3,
        'max_new_tokens': 1024
    }

    response = requests.post(URI, json=dict(input=request), headers = {
        "Authorization": f"Bearer {os.environ['RUNPOD_AI_API_KEY']}"
    })

    if response.status_code == 200:
        data = response.json()
        task_id = data.get('id')
        return wait_for_output(task_id)


def wait_for_output(task_id):
    try:
        url = f"https://api.runpod.ai/v2/{endpoint_id}/status/{task_id}"
        headers = {
            "Authorization": f"Bearer {os.environ['RUNPOD_AI_API_KEY']}"
        }

        while True:
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                data = response.json()
                print(data)
                if data.get('status') == 'COMPLETED':
                    return data['output']
            elif response.status_code >= 400:
                logging.error(response.json())
            # Sleep for 2 seconds between each request
            sleep(2)
    except Exception as e:
        print(e)

```
</details>