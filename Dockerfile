FROM quay.io/jupyter/pytorch-notebook:cuda12-python-3.11.9

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

RUN python -m spacy download en_core_web_sm 
