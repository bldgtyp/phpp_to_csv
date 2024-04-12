from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd


app = FastAPI()

origins = [
    "http://localhost:3000",
    "localhost:3000",
    "https://ph-tools.github.io",
    "https://bldgtyp.github.io",
]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/server_ready")
def awake():
    return {"message": "Server is ready"}


@app.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    if not file:
        return {"error": "No file provided"}

    # Check if the uploaded file is an Excel file
    filename = file.filename or ""
    if not filename.endswith(".xlsx"):
        return {"error": "Only Excel files (xlsx) are allowed"}

    # Read the Excel file using Pandas
    try:
        df = pd.read_excel(file.file)
    except Exception as e:
        return {"error": f"Error reading Excel file: {str(e)}"}

    # Assuming you want to return the data from cell A1
    try:
        cell_data = df.columns[0]
    except Exception as e:
        return {"error": f"Error accessing cell data: {str(e)}"}

    return {"data": cell_data}
