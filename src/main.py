import os
from pathlib import Path
import tempfile
from typing import Annotated, cast
from fastapi import FastAPI, UploadFile
from fastapi.responses import FileResponse, RedirectResponse
from pypdf import PdfWriter, PdfReader, Transformation
from fastapi.staticfiles import StaticFiles
from fastapi.openapi.docs import (
    get_swagger_ui_html
)

app = FastAPI(
    docs_url = None,
    redoc_url = None,
    debug = True
)

app.mount(
    path = "/static",
    app = StaticFiles(directory = "src/static"),
    name = "static"
)

@app.get(
    path = "/docs",
    include_in_schema = False,
)
def custom_swagger_ui_html():
    return get_swagger_ui_html(
        openapi_url = "/openapi.json",
        title = "pdfwn app",
        oauth2_redirect_url = "/docs/oauth2-redirect",
        swagger_js_url = "/static/swagger-ui-bundle.js",
        swagger_css_url = "/static/swagger-ui.css",
        # swagger_favicon_url = "/static/favicon.png"
)

@app.get(
    "/",
    include_in_schema = False
)
async def root():
    return RedirectResponse("docs")

@app.post("/")
async def upload(
    file: UploadFile,
):
    extension = os.path.splitext(file.filename)[1]
    _, path = tempfile.mkstemp(
        prefix = "wm_",
        suffix = extension
    )

    with open(path, 'ab') as f:
        for chunk in iter(lambda: file.file.read(10000), b''):
            f.write(chunk)

    stamp = PdfReader("/app/src/static/bg.pdf").pages[0]
    writer = PdfWriter(clone_from = path)

    os.close(_)
    os.remove(path)

    for page in writer.pages:
        page.merge_page(
            stamp,
            over = True
        )

    writer.write(path)

    return FileResponse(
        path = path,
        filename = os.path.basename(path),
        media_type="multipart/form-data")
    