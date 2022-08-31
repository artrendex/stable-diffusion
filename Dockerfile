FROM python:3.8
RUN pip install cython
COPY requirements.txt ./requirements.txt
RUN pip install -r requirements.txt
WORKDIR /app
COPY . .
RUN pip install -e .
RUN python scripts/preload_models.py
CMD ["python", "entry/main.py", "--address", "0.0.0.0:6000", "serve"]
EXPOSE 6000

