# Use the official Python 3.10 slim image as the base image
FROM python:3.11-slim

COPY . .
# Install system dependencies
RUN apt-get update && apt-get install -y \
    wget \
    bzip2 \
    ca-certificates \
    curl \
    git \
    build-essential \
    autoconf \
    && rm -rf /var/lib/apt/lists/*


RUN apt-get update && \
    apt-get install -y g++ gcc gdb && \
    git clone https://github.com/intel/intel-extension-for-transformers.git && \
    cd intel-extension-for-transformers && \
    git checkout 3e7e3530dcc0b6fb714cbb632fcb0d66ca2604c9 && \
    pip3 install -r requirements.txt && \
    python setup.py install

# Set environment variables
ENV LD_PRELOAD="/usr/lib/x86_64-linux-gnu/libstdc++.so.6"

# Install additional requirements from the requirements.txt file within the Conda environment
RUN pip install -r requirements.txt

# Expose port 8000
EXPOSE 8000

CMD exec uvicorn app.server:app --host 0.0.0.0 --port 8000