from typing import Annotated, Callable, Coroutine
import marimo
from fastapi.responses import HTMLResponse, RedirectResponse, FileResponse
from fastapi import FastAPI, Form, Request, Response
import mimetypes
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

def get_media_type(file_name: str):
    mime_type, _ = mimetypes.guess_type(file_name)
    return mime_type or 'application/octet-stream'  # Default to binary if unknown

@app.get("/download-file/{file_name}")
async def download_file(file_name: str):
    file_path = f"./docs/{file_name}"
    if os.path.exists(file_path):
        # For example:
        # For "document.pdf" - media_type would be "application/pdf"
        # For "document.docx" - media_type would be "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        # For "document.doc" - media_type would be "application/msword"
        return FileResponse(
            file_path,
            media_type=get_media_type(file_name),
            filename=file_name
        )
    raise HTTPException(status_code=404, detail=f"Document not found [./docs/{file_name}]")

## Create a route to download a file
#@app.get("/download-file/{file_name}")
#async def download_file(file_name: str):
#    # Assuming files are stored in a 'docs' directory
#    file_path = f"./docs/{file_name}"
#
#    if os.path.exists(file_path):
#        return FileResponse(
#            file_path,
#            media_type='application/pdf',
#            filename=file_name
#        )
#    return {"error": f"Document not found [./docs/{file_name}]"}, 404

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

