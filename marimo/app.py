from typing import Annotated, Callable, Coroutine
from fastapi.responses import HTMLResponse, RedirectResponse
import marimo
from fastapi import FastAPI, Form, Request, Response
import os
work_dir = os.environ.get('PYCEK_WORKDIR', '/tmp/')

# Create a marimo asgi app
server = (
    marimo.create_asgi_app()
    .with_app(path="", root="./index.py")
    .with_app(path="/bc", root="./bomb_calorimetry.py")
    .with_app(path="/cv", root="./crystal_violet.py")
    .with_app(path="/stats", root="./statistics_lab.py")
    .with_app(path="/surface", root="./surface_adsorption.py")
)

# Create a FastAPI app
app = FastAPI()

app.mount("/", server.build())

# Run the server
if __name__ == "__main__":
    import uvicorn
    os.chdir(work_dir)

    uvicorn.run(app, host="0.0.0.0", port=8000)
