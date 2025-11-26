FROM python:3.13.7


WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "handlers:app", "--host", "0.0.0.0", "--port", "8000"]
