from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..database import SessionLocal
from sqlalchemy import text

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/metrics/hired-by-quarter")
def hired_by_quarter(db: Session = Depends(get_db)):
    query = """
        SELECT 
            d.deparment AS department,
            j.job AS job,
            COUNT(CASE WHEN EXTRACT(QUARTER FROM e.hire_date) = 1 THEN 1 END) AS Q1,
            COUNT(CASE WHEN EXTRACT(QUARTER FROM e.hire_date) = 2 THEN 1 END) AS Q2,
            COUNT(CASE WHEN EXTRACT(QUARTER FROM e.hire_date) = 3 THEN 1 END) AS Q3,
            COUNT(CASE WHEN EXTRACT(QUARTER FROM e.hire_date) = 4 THEN 1 END) AS Q4
        FROM employees e
        JOIN departments d ON e.department_id = d.id
        JOIN jobs j ON e.job_id = j.id
        WHERE EXTRACT(YEAR FROM e.hire_date) = 2021
        GROUP BY d.deparment, j.job
        ORDER BY d.deparment, j.job;
    """
    result = db.execute(text(query)).mappings().all()
    return [dict(row) for row in result]

@router.get("/metrics/above-average-hires")
def above_average_hires(db: Session = Depends(get_db)):
    query = """
        WITH hires_per_department AS (
            SELECT 
                d.id,
                d.deparment AS department,
                COUNT(e.id) AS hired
            FROM employees e
            JOIN departments d ON e.department_id = d.id
            WHERE EXTRACT(YEAR FROM e.hire_date) = 2021
            GROUP BY d.id, d.deparment
        ),
        mean_hires AS (
            SELECT AVG(hired) AS mean_hired FROM hires_per_department
        )
        SELECT 
            h.id,
            h.department,
            h.hired
        FROM hires_per_department h
        JOIN mean_hires m ON h.hired > m.mean_hired
        ORDER BY h.hired DESC;
    """
    result = db.execute(text(query)).mappings().all()
    return [dict(row) for row in result]
