import io
import pandas as pd
from fastapi import UploadFile, HTTPException


MAX_ROWS = 5000  # Aura free safety guard


def parse_csv(file: UploadFile) -> pd.DataFrame:
    name = (file.filename or "").lower()
    raw = file.file.read()
    buf = io.BytesIO(raw)
    try:
        if name.endswith(".csv"):
            df = pd.read_csv(buf)
        elif name.endswith((".xlsx", ".xls")):
            df = pd.read_excel(buf)
        else:
            raise HTTPException(400, f"Unsupported file format: {name}")
    except Exception as e:
        raise HTTPException(400, f"Failed to parse file: {e}")

    if len(df) > MAX_ROWS:
        raise HTTPException(
            413,
            f"Dataset too large ({len(df)} rows). "
            f"Cap is {MAX_ROWS} for hackathon demo.",
        )

    df.columns = [str(c).strip() for c in df.columns]
    return df
