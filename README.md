# Get CSV Files from PHPP 
 Read in a PHPP Excel file and generate CSV files of the data:


 #### [https://bldgtyp.github.io/phpp_to_csv/](https://bldgtyp.github.io/phpp_to_csv/)

# Backend (FastAPI)
#### Setup:
1. `python3.11 -m venv .venv` *(Note: Render.com uses Python3.11, so stick with that)*
1. `source .venv/bin/activate`
1. `pip install -r requirements.txt`
#### Run:
1. `uvicorn backend.main:app --reload`


# Frontend (React)
#### Setup:
1. `npm init -y`
1. `npm install react react-dom`
#### Run:
1. `npm start`


# Deployment as Webservice
1. Make sure origins = [..., "https://bldgtyp.github.io"] is set in [`main.py`](https://github.com/bldgtyp/phpp_to_csv/blob/main/backend/main.py) to fix CORS
1. Push changes to [GitHub](https://github.com/bldgtyp/phpp_to_csv)
1. [Render.com](https://render.com/) | Settings:
    - Name: `phpp_to_csv`
    - Build command: `pip install -r requirements.txt`
    - Start command: `uvicorn backend.main:app --host 0.0.0.0 --port $PORT`
1. Manually Deployment
1. View the live webservice on [https://phpp-to-csv.onrender.com/](https://phpp-to-csv.onrender.com/)
