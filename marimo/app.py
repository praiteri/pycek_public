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
    .with_app(path="/eq", root="./equilibrium.py")
    .with_app(path="/surface", root="./surface_adsorption.py")
)

# Create a route to download a file
@app.get("/download-pdf/{pdf_name}")
async def download_pdf(pdf_name: str):
    # Assuming PDFs are stored in a 'pdfs' directory
    pdf_path = f"./pdfs/{pdf_name}"

    if os.path.exists(pdf_path):
        return FileResponse(
            pdf_path,
            media_type='application/pdf',
            filename=pdf_name
        )
    return {"error": f"PDF not found [./pdfs/{pdf_name}]"}, 404

@app.get("/calendar", response_class=HTMLResponse)
async def read_root():
    with open('calendar.html', 'r', encoding='utf-8') as f:
        return f.read()


## Custom route to serve HTML files that open in a new tab
#@app.route("/html/<filename>")
#def serve_html_file(filename):
#    # Define the directory where your HTML files are stored
#    # This assumes they're in a folder named 'html_files' in the same directory as your app
#    html_dir = Path(os.path.dirname(os.path.abspath(__file__))) / "html_files"
#
#    # Construct the full path to the requested HTML file
#    file_path = html_dir / filename
#
#    # Check if the file exists
#    if not file_path.exists():
#        return "File not found", 404
#
#    # Read the HTML content
#    with open(file_path, "r") as f:
#        html_content = f.read()
#
#    # Set response headers to allow the content to be displayed in the browser
#    headers = {
#        "Content-Type": "text/html",
#        "Content-Disposition": "inline"  # This ensures it displays in browser rather than downloading
#    }
#
#    return html_content, 200, headers


# Mount the marimo server at the root
# This will handle all the routes defined in the marimo server
app.mount("", marimo_server.build())

# Run the server
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

