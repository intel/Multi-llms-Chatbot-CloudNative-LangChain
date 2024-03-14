FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /usr/

COPY requirements.txt ./

# Upgrade pip and install dependencies
RUN pip install --upgrade pip && \
    pip install -r requirements.txt &&\
    pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu

COPY ./app ./app

EXPOSE 5005

CMD exec uvicorn app.server:app --host 0.0.0.0 --port 5005