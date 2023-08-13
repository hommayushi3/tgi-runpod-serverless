FROM ghcr.io/huggingface/text-generation-inference:1.0.0

RUN pip install --upgrade pip && \
    pip install text-generation runpod

RUN mkdir data
WORKDIR /data

COPY handler.py /data/handler.py
COPY entrypoint.sh /data/entrypoint.sh

RUN chmod +x /data/entrypoint.sh

ENTRYPOINT [ "./entrypoint.sh" ]
