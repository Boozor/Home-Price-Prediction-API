# Stage 1: Build and test
FROM python:3.11-slim AS builder

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code and inputs
COPY app.py .
COPY features.json .
COPY home_price_model.pkl .
COPY inputs/ ./inputs/
COPY tests/ ./tests/ 

# Copy ALL files (debugging)
COPY . .

# Verify inputs/ folder exists (debugging step)
RUN ls -la inputs/

# Run tests (ensure inputs/ and tests/ exist)
RUN pytest tests/

# Stage 2: Final image
FROM python:3.11-slim

WORKDIR /app

# **Install curl**
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

# Copy ONLY runtime-essential files from the builder
COPY --from=builder /app/requirements.txt .
COPY --from=builder /app/app.py .
COPY --from=builder /app/features.json .
COPY --from=builder /app/home_price_model.pkl .
COPY --from=builder /app/inputs/ ./inputs/
COPY --from=builder /app/tests/ ./tests/

# Install runtime dependencies (no test dependencies!)
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 50505
CMD ["gunicorn", "--bind", "0.0.0.0:50505", "--access-logfile", "-", "--error-logfile", "-", "app:app"]