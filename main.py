from fastapi import FastAPI
from mangum import Mangum

app = FastAPI(title="FastAPI on Lambda via ECR")

@app.get("/")
def read_root():
    return {"message": "Hello from FastAPI on AWS Lambda!"}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: str | None = None):
    return {"item_id": item_id, "query": q}

# Lambda用のハンドラー
handler = Mangum(app)
