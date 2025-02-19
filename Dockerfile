FROM python:3.12-slim as builder
COPY --from=ghcr.io/astral-sh/uv:0.4.20 /uv /bin/uv
COPY ./deployment/requirements.txt requirements.txt
RUN uv pip install -r requirements.txt \
    && rm -rf /root/.cache/pip/*

# Install and cleanup in one layer
COPY ./ /pycek_public
RUN uv pip install /pycek_public \
    && rm -rf /pycek_public \
    && rm -rf /root/.cache/* 

FROM python:3.12-slim
RUN useradd -m -u 1000 user
COPY --from=builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
WORKDIR /app
COPY --chown=user ./marimo /app
RUN chown -R user:user /app
USER user

ENV PYCEK_WORKDIR="/data"
WORKDIR /app
CMD ["python", "app.py"]
