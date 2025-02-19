FROM python:3.12
COPY --from=ghcr.io/astral-sh/uv:0.4.20 /uv /bin/uv
RUN useradd -m -u 1000 user
ENV PATH="/home/user/.local/bin:$PATH"

ENV UV_SYSTEM_PYTHON=1
ENV PYCEK_WORKDIR=/tmp
WORKDIR /app
COPY --chown=user ./deployment/requirements.txt requirements.txt
RUN uv pip install -r requirements.txt

# Copy and install the local repo, then remove it
COPY --chown=user ./ /pycek_public
RUN uv pip install /pycek_public && rm -rf /pycek 
COPY --chown=user ./marimo /app
RUN chown -R user:user /app
USER user
CMD ["python", "app.py"]
