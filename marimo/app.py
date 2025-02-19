from typing import Annotated, Callable, Coroutine
from fastapi.responses import HTMLResponse, RedirectResponse
import marimo
from fastapi import FastAPI, Form, Request, Response
import os

# Create a FastAPI app
app = FastAPI()

# Index route that serves the HTML file
@app.get("/", response_class=HTMLResponse)
async def read_root():
    with open('index.html', 'r', encoding='utf-8') as f:
        return f.read()

# Create a marimo asgi app with all routes
marimo_server = (
    marimo.create_asgi_app()
    .with_app(path="/bc", root="./bomb_calorimetry.py")
    .with_app(path="/cv", root="./crystal_violet.py")
    .with_app(path="/stats", root="./statistics_lab.py")
    .with_app(path="/surface", root="./surface_adsorption.py")
)

# Mount the marimo server at the root
# This will handle all the routes defined in the marimo server
app.mount("", marimo_server.build())

# Run the server
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

#from typing import Annotated, Callable, Coroutine
#from fastapi.responses import HTMLResponse, RedirectResponse
#import marimo
#from fastapi import FastAPI, Form, Request, Response
#
#
## Create a marimo asgi app
#server = (
#    marimo.create_asgi_app()
#    .with_app(path="", root="./index.py")
#    .with_app(path="/bc", root="./bomb_calorimetry.py")
#    .with_app(path="/cv", root="./crystal_violet.py")
#    .with_app(path="/stats", root="./statistics_lab.py")
#    .with_app(path="/surface", root="./surface_adsorption.py")
#)
#
## Create a FastAPI app
#app = FastAPI()
#
#app.mount("/", server.build())
#
## Run the server
#if __name__ == "__main__":
#    import uvicorn
#
#    uvicorn.run(app, host="0.0.0.0", port=8000)
