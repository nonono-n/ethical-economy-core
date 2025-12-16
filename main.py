import json
import os
import psycopg2
import boto3
from fastapi import FastAPI
from mangum import Mangum

app = FastAPI(title="FastAPI on Lambda via ECR")

@app.get("/")
def read_root():
    return {"message": "Hello from FastAPI on AWS Lambda!"}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: str | None = None):
    return {"item_id": item_id, "query": q}

def get_db_info():
    secret_name = os.environ["SECRET_NAME"]
    region_name = "ap-southeast-2"

    client = boto3.client("secretsmanager", region_name=region_name)
    response = client.get_secret_value(SecretId=secret_name)

    secret = json.loads(response["SecretString"])
    return secret

@app.get("/secrettest")
def secrettest():
    secret = get_db_info()
    return {"ok": True, "keys": list(secret.keys())}

@app.get("/dbtest")
def dbtest():
    try:
        secret = get_db_info()

        conn = psycopg2.connect(
            host=secret["host"],
            dbname=secret["dbname"],
            user=secret["user"],
            password=secret["password"],
            port=int(secret["port"]),
            connect_timeout=5,  # 追加
        )

        cur = conn.cursor()
        cur.execute("SELECT version();")
        version = cur.fetchone()
        cur.close()
        conn.close()

        return {
            "status": "connected",
            "postgres_version": version[0]
        }

    except Exception as e:
        return {"status": "error", "detail": str(e)}

# Lambda用のハンドラー
handler = Mangum(app, api_gateway_base_path="/default")

