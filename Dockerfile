# Base image with Python 3.9
FROM ghcr.io/huggingface/text-generation-inference:1.0.2 as base

RUN python -c "import urllib.request; urllib.request.urlretrieve('https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh', 'miniconda.sh')" && \
    bash miniconda.sh -b -p $HOME/miniconda && \
    eval "$(/root/miniconda/bin/conda shell.bash hook)" && \
    rm miniconda.sh

# Create a new environment with Python 3.10
RUN conda create --name py310 python=3.10

# Install runpod for Python 3.10
RUN conda run -n py310 pip install install runpod text-generation

WORKDIR /usr/src

COPY handler.py /usr/src/handler.py
COPY entrypoint.sh /usr/src/entrypoint.sh

RUN chmod +x /usr/src/entrypoint.sh

ENV HUGGINGFACE_HUB_CACHE /runpod-volume/hub
ENV TRANSFORMERS_CACHE /runpod-volume/hub

ENTRYPOINT [ "./entrypoint.sh" ]
