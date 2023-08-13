FROM ghcr.io/huggingface/text-generation-inference:latest

RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y git && \
    apt-get clean

RUN /opt/conda/bin/conda create -n runpod-tgi python=3.10 -y && \
    /opt/conda/bin/conda activate runpod-tgi && \
    /opt/conda/bin/conda install -c "${INSTALL_CHANNEL}" -c "${CUDA_CHANNEL}" pytorch==$PYTORCH_VERSION "pytorch-cuda=$(echo $CUDA_VERSION | cut -d'.' -f 1-2)"  ;; \
    esac && \
    /opt/conda/bin/conda clean -ya && \
    /opt/conda/bin/conda install -c "nvidia/label/cuda-11.8.0"  cuda==11.8 && \
    /opt/conda/bin/conda clean -ya

RUN cd server && \
    make gen-server && \
    pip install -r requirements.txt && \
    pip install ".[bnb, accelerate, quantize]" text-generation git+https://github.com/runpod/runpod-python.git --no-cache-dir

WORKDIR /usr/src

COPY handler.py /usr/src/handler.py
COPY entrypoint.sh /usr/src/entrypoint.sh

RUN chmod +x /usr/src/entrypoint.sh

ENV HUGGINGFACE_HUB_CACHE /runpod-volume/hub
ENV TRANSFORMERS_CACHE /runpod-volume/hub

ENTRYPOINT [ "./entrypoint.sh" ]
