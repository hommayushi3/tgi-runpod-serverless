import os
import requests
from time import sleep
import argparse
import sys
import json


endpoint_id = os.environ["RUNPOD_ENDPOINT_ID"]
URI = f"https://api.runpod.ai/v2/{endpoint_id}/run"
HEADERS = {"Authorization": f"Bearer {os.environ['RUNPOD_AI_API_KEY']}"}

def run(prompt, params={}, stream=False, request_delay=None):
    request = {
        'prompt': prompt,
        'generate_params': params,
        'stream': stream
    }

    response = requests.post(URI, json=dict(input=request), headers=HEADERS)

    if response.status_code == 200:
        data = response.json()
        task_id = data.get('id')
        return wait_for_output(task_id, stream=stream, request_delay=request_delay or 0.2)


def cancel_task(task_id):
    url = f"https://api.runpod.ai/v2/{endpoint_id}/cancel/{task_id}"
    response = requests.get(url, headers=HEADERS)
    return response


def wait_for_output(task_id, stream=False, request_delay=0.2):
    url = f"https://api.runpod.ai/v2/{endpoint_id}/stream/{task_id}"
    previous_output = ''

    try:
        while True:
            response = requests.get(url, headers=HEADERS)
            if response.status_code == 200:
                data = response.json()
                if len(data['stream']) > 0:
                    new_output = data['stream'][0]['output']

                    if stream:
                        sys.stdout.write(new_output)
                        sys.stdout.flush()
                    previous_output = new_output
                
                if data.get('status') == 'COMPLETED':
                    if not stream:
                        return previous_output
                    break
                    
            elif response.status_code >= 400:
                print(response)
            # Sleep for request_delay seconds between each request
            sleep(request_delay)
    except Exception as e:
        print("Error:", e)
        cancel_task(task_id)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Runpod AI CLI')
    parser.add_argument('-s', '--stream', action='store_true', help='Stream output')
    parser.add_argument('-p', '--params_json', type=str, help='JSON string of generation params')
    parser.add_argument('-d', '--request_delay', type=float, help='Number of seconds to wait between each status check')
    prompt = """### Instruction:
From the following clinical notes, what tests, diagnoses, and recommendations should the I give? Provide your answer as a detailed report with labeled sections "Diagnostic Tests", "Possible Diagnoses", and "Patient Recommendations".

Input: 17-year-old male, has come to the student health clinic complaining of heart pounding. Mr. Cleveland's mother has given verbal consent for a history, physical examination, and treatment
- began 2-3 months ago,sudden,intermittent for 2 days(lasting 3-4 min),worsening,non-allev/aggrav
- associated with dispnea on exersion and rest,stressed out about school
- reports fe feels like his heart is jumping out of his chest
- ros:denies chest pain,dyaphoresis,wt loss,chills,fever,nausea,vomiting,pedal edeam
- pmh:non,meds :aderol (from a friend),nkda
- fh:father had MI recently,mother has thyroid dz
- sh:non-smoker,mariguana 5-6 months ago,3 beers on the weekend, basketball at school
- sh:no std,no other significant medical conditions.

### Response:
"""
    args = parser.parse_args()
    print(run(prompt, params=json.loads(args.params_json), stream=args.stream, request_delay=args.request_delay))
