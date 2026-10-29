import json
import os
from fastapi import HTTPException


file_path = os.path.join(
    os.path.dirname(os.path.dirname(__file__)),
    "data",
    "data.json",
)

def load_json():
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")

    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)
