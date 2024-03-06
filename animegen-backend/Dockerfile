FROM python:3.12.2-bookworm

# Install supervisord
RUN apt-get update && \
    apt-get install -y supervisor && \
    rm -rf /var/lib/apt/lists/*


RUN mkdir -p /var/log/supervisor /var/log/animegen
ENV PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True
WORKDIR /app

COPY ./requirements.txt .

RUN pip install -r requirements.txt
RUN pip install "fastapi[all]"
RUN pip install pydantic==1.10.13
RUN pip uninstall -y torch
RUN pip uninstall -y torchvision
RUN pip install torch torchvision --index-url https://download.pytorch.org/whl/cu118



COPY . .


EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
