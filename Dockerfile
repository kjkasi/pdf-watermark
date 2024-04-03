FROM python:3.10

WORKDIR /app

COPY ./requirements.txt /app/requirements.txt

RUN python -m pip install -r requirements.txt
RUN python -m pip install --disable-pip-version-check debugpy -t /tmp

EXPOSE 80

ENTRYPOINT [ "python", "/tmp/debugpy", "--listen", "0.0.0.0:5679", "-m", "uvicorn", "--reload", "--proxy-headers", "--host", "0.0.0.0", "--port", "80", "src.main:app" ]