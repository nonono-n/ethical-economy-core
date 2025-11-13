# ---- ベースイメージ（AWS Lambda公式）----
FROM public.ecr.aws/lambda/python:3.10

# ---- 依存パッケージのコピーとインストール ----
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# ---- アプリ本体をコピー ----
COPY main.py .

# ---- Lambdaエントリーポイント ----
# （handlerはmain.py内のMangumインスタンス名）
CMD ["main.handler"]
