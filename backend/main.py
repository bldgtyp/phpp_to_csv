import pandas as pd
from typing import Union
import zipfile
from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import StreamingResponse
import io

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
def awake() -> dict[str, str]:
    return {"message": "Server is ready"}


@app.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    if not file:
        return {"error": "No file provided?"}

    # Ensure the uploaded file is an Excel file
    filename = file.filename or ""
    if not filename.endswith(".xlsx"):
        return {"error": "Sorry, only Excel files (xlsx) are allowed."}

    # Read the Excel file using Pandas
    try:
        xls = pd.read_excel(file.file, sheet_name=None)
    except Exception as e:
        return {"error": f"Sorry, there was an error reading the Excel file: {str(e)}"}

    # Create a zip file in memory
    memory_file = io.BytesIO()
    with zipfile.ZipFile(memory_file, "w") as zf:
        # Loop through each sheet in the Excel file
        for sheet_name, df in xls.items():
            # Convert the DataFrame to a CSV file and save it in the zip file
            csv = df.to_csv(index=False)
            zf.writestr(f"{sheet_name}.csv", csv)

    memory_file.seek(0)

    # Create a StreamingResponse to return the zip file
    response = StreamingResponse(memory_file, media_type="application/zip")
    response.headers["Content-Disposition"] = "attachment; filename=output.zip"

    return response
