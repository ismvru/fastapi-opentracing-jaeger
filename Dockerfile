FROM python:3-slim as wheeler
WORKDIR /whl
COPY requirements.txt /whl/
RUN pip wheel -r requirements.txt

FROM python:3-slim
WORKDIR /whl
COPY --from=wheeler /whl/*.whl /app/
RUN pip --no-cache-dir install /app/*.whl
WORKDIR /app
COPY main.py /app/
CMD ["python3", "main.py"]