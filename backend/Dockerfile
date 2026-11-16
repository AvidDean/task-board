# ==========================================
# STAGE 1: Builder
# ==========================================
FROM python:3.12-slim AS builder

# Do not write .pyc files; show logs immediately
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Create an isolated virtual environment for dependencies
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Install dependencies inside the virtual environment
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt


# ==========================================
# STAGE 2: Runner (Final Minimal Image)
# ==========================================
FROM python:3.12-slim AS runner

# Preserve Python logging and runtime environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PATH="/opt/venv/bin:$PATH"

WORKDIR /app

# Run as a normal user, not root
RUN useradd --create-home appuser

# Copy ONLY the pre-installed packages from the builder stage
COPY --from=builder /opt/venv /opt/venv

# Copy application source code
COPY app.py .

# Ensure app directory permissions belong to appuser
RUN chown -R appuser:appuser /app

USER appuser

EXPOSE 5000
# 0.0.0.0 means "listen on every address inside the container".
# Never change this to localhost or 127.0.0.1: the container would stop answering.
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "2", "app:app"]