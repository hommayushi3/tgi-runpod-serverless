FROM ghcr.io/huggingface/text-generation-inference:latest

RUN  pip install runpod text-generation --no-cache-dir

WORKDIR /usr/src

COPY handler.py /usr/src/handler.py
COPY entrypoint.sh /usr/src/entrypoint.sh

RUN chmod +x /usr/src/entrypoint.sh

ENV HUGGINGFACE_HUB_CACHE /runpod-volume/hub
ENV TRANSFORMERS_CACHE /runpod-volume/hub

ENTRYPOINT [ "./entrypoint.sh" ]
