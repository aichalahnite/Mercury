FROM python:3.12-slim

# Security best practices
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Install needed tools including netcat
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    netcat-openbsd \
    curl \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

# Use pinned dependencies + disable pip cache
RUN pip install --no-cache-dir -r requirements.txt

# Add non-root user
RUN addgroup --system appgroup && \
    adduser --system --ingroup appgroup appuser

COPY . .

# Apply correct permissions
RUN chown -R appuser:appgroup /app

USER appuser

# Entry script
CMD ["./entrypoint.sh"]
