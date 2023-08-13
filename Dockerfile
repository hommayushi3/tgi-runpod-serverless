FROM ghcr.io/huggingface/text-generation-inference:latest

RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y git && \
    apt-get clean

RUN /opt/conda/bin/conda uninstall python -y && \
    /opt/conda/bin/conda install python=3.10 -y && \
    /opt/conda/bin/conda clean -a -y

RUN pip install --upgrade pip && \
    pip install text-generation git+https://github.com/runpod/runpod-python.git

RUN mkdir data
WORKDIR /data

COPY handler.py /data/handler.py
COPY entrypoint.sh /data/entrypoint.sh

RUN chmod +x /data/entrypoint.sh

ENV HUGGINGFACE_HUB_CACHE /runpod-volume/hub
ENV TRANSFORMERS_CACHE /runpod-volume/hub

ENTRYPOINT [ "./entrypoint.sh" ]
