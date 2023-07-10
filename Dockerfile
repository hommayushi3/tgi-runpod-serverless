FROM ghcr.io/huggingface/text-generation-inference:latest

RUN pip install --upgrade pip && \
    pip install text-generation

RUN mkdir data
WORKDIR /data

ENV PROMPT_PREFIX=""
ENV PROMPT_SUFFIX=""

COPY handler.py /data/handler.py
COPY entrypoint.sh /data/entrypoint.sh

RUN chmod +x /data/entrypoint.sh

ENTRYPOINT [ "./entrypoint.sh" ]
