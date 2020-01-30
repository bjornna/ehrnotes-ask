FROM tiangolo/uvicorn-gunicorn-fastapi:python3.7
RUN pip install spacy spacy-lookups-data xlrd ipython
RUN python -m spacy download nb_core_news_sm
COPY ./combined.jsonl /app 
COPY ./app /app/app