# Python verification only; not a TeX or Lean build image. Docker was not run here.
FROM python:3.12-slim-bookworm@sha256:fc169880a4d941f3142c0e2e623f05f246150add19dc36fc9224df20fb19e5fd
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 PIP_DISABLE_PIP_VERSION_CHECK=1
WORKDIR /app
COPY requirements.txt requirements.lock ./
RUN python -m pip install --no-cache-dir --require-hashes -r requirements.txt
COPY . .
RUN mkdir -p /app/results && chown -R 10001:10001 /app
USER 10001:10001
CMD ["python", "RAP_Master_Verification.py", "--output", "results/master-verification.json"]
