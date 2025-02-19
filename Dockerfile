FROM python:3.12
COPY --from=ghcr.io/astral-sh/uv:0.4.20 /uv /bin/uv
RUN useradd -m -u 1000 user
ENV PATH="/home/user/.local/bin:$PATH"

ENV UV_SYSTEM_PYTHON=1
WORKDIR /app

# Copy and install the local repo, then remove it
RUN uv pip install git+https://github.com/praiteri/pycek_public
RUN uv pip install marimo fastapi colorama
COPY --chown=user ./marimo /app
RUN chown -R user:user /app
USER user
ENV PYCEK_WORKDIR=/tmp
CMD ["python", "app.py"]
