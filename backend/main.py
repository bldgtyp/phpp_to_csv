# -*- coding: utf-8 -*-
# -*- Python Version: 3.11 -*-

import io
import traceback
import zipfile

from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import StreamingResponse

from backend.read_phpp import load_phpp_data
from backend.write_csv import create_csv_files_from_phpp_data

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

# TODO: get these as user-defined inputs
CO2E_LIMIT_TONS_YEAR = 5.0  # <-- into the PHPP....
OMITTED_ASSEMBLIES: list[str] = []


@app.get("/server_ready")
def awake() -> dict[str, str]:
    """Check if the server is ready to go."""
    return {"message": "Server is ready"}


@app.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    """Upload a PHPP Excel file and return a .ZIP file containing .CSV files of the data."""

    # -------------------------------------------------------------------------
    # Check th uploaded file is an Excel file
    if not file:
        return {"error": "No file provided?"}

    filename = file.filename or ""
    if not filename.endswith(".xlsx"):
        return {"error": "Sorry, only Excel files (xlsx) are allowed."}

    # -------------------------------------------------------------------------
    # Read in the Excel file using Pandas and output the PHPP-Data
    try:
        phpp_data = load_phpp_data(file.file)
    except Exception as e:
        error_info = traceback.format_exc()
        print(f"Error: {error_info}")
        return {"error": f"Sorry, there was an error reading the Excel file: {str(e)}"}

    # -------------------------------------------------------------------------
    # Create the CSV files from the PHPP-Data in memory
    try:
        csv_files = create_csv_files_from_phpp_data(
            phpp_data,
            CO2E_LIMIT_TONS_YEAR,
            OMITTED_ASSEMBLIES,
        )
    except KeyError as e:
        error_info = traceback.format_exc()
        print(f"Error: {error_info}")
        raise HTTPException(status_code=500, detail=f"Sorry, there was an error creating the CSV file: {str(e)}")
    except Exception as e:
        error_info = traceback.format_exc()
        print(f"Error: {error_info}")
        raise HTTPException(status_code=500, detail=f"Sorry, there was an error creating the CSV files: {str(e)}")

    # -------------------------------------------------------------------------
    # Create a .zip file in memory
    memory_file = io.BytesIO()
    with zipfile.ZipFile(memory_file, "w") as zf:
        # Loop through each CSV name and data-string in the collection
        # and add each CSV file data to the .zip file
        for file_name, csv_file in csv_files:
            zf.writestr(f"{file_name}.csv", csv_file)

    # -------------------------------------------------------------------------
    # Create a StreamingResponse to return the zip file
    # Reset the memory file pointer to the start before steaming it back
    memory_file.seek(0)
    response = StreamingResponse(memory_file, media_type="application/zip")
    response.headers["Content-Disposition"] = "attachment; filename=output.zip"

    return response
