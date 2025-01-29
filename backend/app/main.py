# backend/app/main.py
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
import pytesseract
from pyzbar.pyzbar import decode
from PIL import Image
import sqlite3
import os

app = FastAPI()

# Database setup
DATABASE = "receipts.db"

def init_db():
    with sqlite3.connect(DATABASE) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS receipts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                product TEXT,
                price REAL,
                barcode TEXT
            )
        """)

@app.post("/upload")
async def upload_receipt(file: UploadFile = File(...)):
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Invalid file type. Please upload an image.")

    try:
        image = Image.open(file.file)
        text = pytesseract.image_to_string(image)
        barcodes = decode(image)

        # Extract product details and prices (simplified for demo)
        products = [line for line in text.split("\n") if "£" in line]
        barcode_numbers = [barcode.data.decode("utf-8") for barcode in barcodes]

        # Save to database
        with sqlite3.connect(DATABASE) as conn:
            cursor = conn.cursor()
            for product, barcode in zip(products, barcode_numbers):
                cursor.execute("INSERT INTO receipts (product, price, barcode) VALUES (?, ?, ?)",
                               (product, float(product.split("£")[-1]), barcode))

        return JSONResponse(content={"data": products, "barcodes": barcode_numbers})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/receipts")
async def get_receipts():
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM receipts")
        receipts = cursor.fetchall()
    return JSONResponse(content={"receipts": receipts})

if __name__ == "__main__":
    init_db()
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)