from fastapi import FastAPI, Request, UploadFile, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from PIL import Image
import os

app = FastAPI()

# Templates
templates = Jinja2Templates(directory="templates")

# Static folder for output images
if not os.path.exists("static/output"):
    os.makedirs("static/output")
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/process", response_class=HTMLResponse)
async def process_image(request: Request, file: UploadFile, operation: str = Form(...)):
    # Save uploaded file temporarily
    file_path = f"static/output/{file.filename}"
    with open(file_path, "wb") as f:
        f.write(await file.read())

    # Open image
    image = Image.open(file_path)

    # Apply operation
    if operation == "grayscale":
        image = image.convert("L")  # Grayscale
    elif operation == "rotate":
        image = image.rotate(90, expand=True)  # Rotate 90 degrees

    # Save processed image
    processed_path = f"static/output/processed_{file.filename}"
    image.save(processed_path)

    return templates.TemplateResponse(
        "index.html",
        {"request": request, "result_image": f"/{processed_path}"}
    )
