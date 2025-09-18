from fastapi import HTTPException, UploadFile
import pandas as pd

def file_contains_term(file_path: str, search_term: str) -> bool:
    """Return true/false if search_term exists in the excel file."""
    try:
        excel = pd.ExcelFile(file_path)
        for sheet in excel.sheet_names:
            df = pd.read_excel(excel, sheet_name=sheet, header=None, dtype=str)
            if search_term in df.values:
                return True
    except Exception:
        return False
    return False

def file_sum_numbers(file_path: str) -> float:
    """Sum all numbers in all sheets in the excel file."""
    sum = 0
    try: 
      excel = pd.ExcelFile(file_path)
      for sheet in excel.sheet_names:
          df = pd.read_excel(excel, sheet_name=sheet, header=None)
          df = df.apply(pd.to_numeric, errors="coerce")
          sum += df.sum().sum(skipna=True)
    except Exception:
        return 0  # skip unreadable/missing files
    return(sum)

def validate_excel_file(file: UploadFile):
    """    Checks if file is a valid excel file."""
    if not file.filename.lower().endswith(".xlsx"):
        raise HTTPException(status_code=400, detail="Only .xlsx files allowed")
    
    try:
        file.file.seek(0)
        xls = pd.ExcelFile(file.file, engine="openpyxl")
        if not xls.sheet_names:
            raise HTTPException(status_code=400, detail="Excel file contains no sheets")
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid or corrupted Excel file")
    finally:
        file.file.seek(0)  # reset pointer for later saving