FROM ghcr.io/huggingface/text-generation-inference:1.0.0

RUN apt update & apt install -y git & apt-get clean

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
