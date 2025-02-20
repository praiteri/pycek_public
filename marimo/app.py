from typing import Annotated, Callable, Coroutine
from fastapi.responses import HTMLResponse, RedirectResponse, FileResponse
import marimo
from fastapi import FastAPI, Form, Request, Response
import os
from pathlib import Path


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

# Create a route to download a file
@app.get("/download-pdf/{pdf_name}")
async def download_pdf(pdf_name: str):
    # Assuming PDFs are stored in a 'pdfs' directory
    pdf_path = f"../pdfs/{pdf_name}"

    if os.path.exists(pdf_path):
        return FileResponse(
            pdf_path,
            media_type='application/pdf',
            filename=pdf_name
        )
    return {"error": f"PDF not found [../pdfs/{pdf_name}]"}, 404

# Create a route to display a pdf
@app.get("/pdf/direct/{pdf_name}")
async def get_pdf_direct(pdf_name: str):
    pdf_path = Path(f"../pdfs/{pdf_name}")

    if not pdf_path.exists():
        raise HTTPException(status_code=404, detail=f"PDF not found {pdf_path}")

    return FileResponse(
        path=pdf_path,
        media_type="application/pdf",
        filename=pdf_name + ".pdf"
    )


# Mount the marimo server at the root
# This will handle all the routes defined in the marimo server
app.mount("", marimo_server.build())

# Run the server
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=2718)

