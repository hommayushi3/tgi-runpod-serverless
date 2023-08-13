# tgi-runpod-serverless

## Summary
This Docker image runs HuggingFace's text-generation-inference on Runpod Serverless.

Modeled off of [worker-vllm](https://github.com/runpod-workers/worker-vllm) repo for RunPod's streaming and continuous batching handling.

## About Huggingface's Text Generation Inference Package
### License
Free for commercial use; requires license for commercial use for versions >= '1.0.0'. See [here](https://github.com/huggingface/text-generation-inference/blob/main/LICENSE) for full details of HFOILv1.0.

### Key Features (See full list [here](https://github.com/huggingface/text-generation-inference#features))
1. Supports a large number of models including Llama, Starcoder, MPT, Falcon and FLAN-T5.
2. Supports most common quantization strategies including GPTQ (both AutoGPTQ and Exllama - for Llama models) and bitsandbytes.
3. Supports Tensor Parallelism for fast multi-gpu inference.
4. Supports continuous batching and paged attention for relevant architectures similar to [vllm repo](https://github.com/vllm-project/vllm).
5. Supports Flash-Attention 2 for relevant architectures on appropriate hardware.

## Set Up
1. Create a RunPod account and navigate to the [RunPod Serverless Console](https://www.runpod.io/console/serverless).
2. (Optional) Create a Network Volume to cache your model to speed up cold starts (but will incur some cost per hour for storage).
    - *Note: Only certain Network Volume regions are compatible with certain instance types on RunPod, so try out if your Network Volume makes your desired instance type Unavailable, try other regions for your Network Volume.*
3. Navigate to `My Templates` and click on the `New Template` button.
4. Enter in the following fields and click on the `Save Template` button:

    | Template Field | Value |
    | --- | --- |
    | Template Name | `TheBloke/LlongOrca-7B-16K-GPTQ-tgi` |
    | Container Image | `hommayushi3/tgi-runpod-serverless:main` |
    | Container Disk | A size large enough to store your libraries + your desired model in 4bit. |

    - Container Disk Size Guide:
        | Model Parameters | Storage & VRAM |
        | --- | --- |
        | 7B | 6GB |
        | 13B | 9GB |
        | 33B | 19GB |
        | 65B | 35GB |
        | 70B | 38GB |

    - Environment Variables:

        | Environment Variable | Example Value |
        | --- | --- |
        | (Required) `MODEL_REPO` | `TheBloke/airoboros-7B-gpt4-1.4-GPTQ` or any other repo for GPTQ Llama model. See https://huggingface.co/models?other=llama&sort=trending&search=thebloke+gptq for other models. Must have `.safetensors` file(s). |

4. Now click on `My Endpoints` and click on the `New Endpoint` button.
5. Fill in the following fields and click on the `Create` button:
    | Endpoint Field | Value |
    | --- | --- |
    | Endpoint Name | `TheBloke/airoboros-7B-gpt4-1.4-GPTQ-tgi` |
    | Select Template | `TheBloke/airoboros-7B-gpt4-1.4-GPTQ-tgi` |
    | Min Provisioned Workers | `0` |
    | Max Workers | `1` |
    | Idle Timeout | `5` seconds |
    | FlashBoot | Checked/Enabled |
    | GPU Type(s) | t |
    | (Optional) Network Volume | `airoboros-7b` |
