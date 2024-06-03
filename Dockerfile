# For more information, please refer to https://aka.ms/vscode-docker-python
FROM python:3.11.4-slim-buster AS base
# Download and install PyTorch
RUN pip install torch torchvision torchaudio -f https://download.pytorch.org/whl/cpu/torch_stable.html
RUN pip install transformers==4.37.2
RUN pip install keras

COPY requirements.txt .
RUN python -m pip install -r requirements.txt
WORKDIR /app
COPY . /app
EXPOSE 5008

# During debugging, this entry point will be overridden. For more information, please refer to https://aka.ms/vscode-docker-python-debug
CMD ["gunicorn", "--bind", "0.0.0.0:5008", "--timeout", "300", "app:app"]
