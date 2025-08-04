from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
import pandas as pd
from sqlalchemy.orm import Session
from ..database import SessionLocal
from .. import models
import numpy as np


router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/upload/{table_name}", response_model=None)
def upload_csv(table_name: str, file: UploadFile = File(...), db: Session = Depends(get_db)):

    if not file.filename.endswith(".csv"):
        raise HTTPException(status_code=400, detail="ReadOnly CSV files.")
    
    if table_name == "employees":
        columns = ["id", "name", "hire_date", "department_id", "job_id"]
    elif table_name == "departments":
        columns = ["id", "deparment"]
    elif table_name == "jobs":
        columns = ["id", "job"]
    else:
        raise HTTPException(status_code=400, detail="Invalid table name.")

    df = pd.read_csv(file.file, header=None, names=columns)

    if list(df.columns) != columns:
        raise HTTPException(status_code=400, detail="CSV columns do not match expected format.")

    if table_name == "departments":
        db.bulk_insert_mappings(models.Department, df.to_dict(orient="records"))
    elif table_name == "jobs":
        db.bulk_insert_mappings(models.Job, df.to_dict(orient="records"))
    elif table_name == "employees":
        df["hire_date"] = pd.to_datetime(df["hire_date"], errors="coerce")
        df["hire_date"] = df["hire_date"].fillna(pd.Timestamp("2000-01-01"))
        # Rellenar otros valores faltantes
        df["name"] = df["name"].fillna("N/A")
        df["job_id"] = pd.to_numeric(df["job_id"], errors="coerce")
        df["department_id"] = pd.to_numeric(df["department_id"], errors="coerce")
        df.replace({np.nan: None}, inplace=True)

        db.bulk_insert_mappings(models.Employee, df.to_dict(orient="records"))
    else:
        raise HTTPException(status_code=400, detail="Invalid table name.")
    
    try:
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Insert failed: {str(e)}")
    return {"status": "success", "rows_inserted": len(df)}
