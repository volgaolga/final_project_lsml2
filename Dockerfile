FROM python:3.9-slim
RUN mkdir /application
WORKDIR /application
COPY static static
COPY templates templates
COPY application.py .
COPY final_project.ipynb .
COPY model_rfc_lsml2.joblib .
COPY requirements.txt .
RUN pip install -r requirements.txt
