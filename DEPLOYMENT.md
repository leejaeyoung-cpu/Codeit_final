# 🚀 AdGen AI Deployment Guide

This guide describes how to deploy the AdGen AI Background Removal Service using Docker.

## Prerequisites

*   Docker installed
*   Docker Compose installed
*   Hugging Face API Token (for RMBG-2.0)
*   (Optional) Google Cloud Service Account Credentials (for GCS upload)

## 1. Environment Setup

### Hugging Face Token
You need a Hugging Face token to access the RMBG-2.0 model via API.
Set it as an environment variable:

**Linux/Mac:**
```bash
export HF_TOKEN=your_token_here
```

**Windows (PowerShell):**
```powershell
$env:HF_TOKEN="your_token_here"
```

### Google Cloud Storage (Optional)
If you want to use GCS for storing processed images:
1.  Place your service account JSON key file in the project root (e.g., `gcs_key.json`).
2.  Update `docker-compose.yml` to mount this file and set `GOOGLE_APPLICATION_CREDENTIALS`.

## 2. Deployment

Build and start the services using Docker Compose:

```bash
docker-compose up -d --build
```

This will start:
*   **API Server**: http://localhost:8000
*   **PostgreSQL**: Port 5432
*   **Redis**: Port 6379
*   **Celery Worker**: Background task processing

## 3. Configuration

The application is configured via environment variables in `docker-compose.yml`.

| Variable | Default | Description |
|----------|---------|-------------|
| `BG_REMOVAL_MODEL` | `rmbg-2.0` | Primary model to use |
| `BG_REMOVAL_USE_LOCAL_MODEL` | `false` | `false` for API, `true` for local model |
| `HF_TOKEN` | - | Required for RMBG-2.0 API |
| `BG_REMOVAL_FALLBACK` | `true` | Fallback to U2-Net if API fails |

## 4. Verification

Check if the service is running:

```bash
curl http://localhost:8000/health
```

Response should be:
```json
{
  "status": "healthy",
  "model_name": "rmbg-2.0-api",
  ...
}
```

## 5. Troubleshooting

### Disk Space Issues
If you encounter "No space left on device" errors during build:
1.  Prune Docker system: `docker system prune -a`
2.  Remove local model files if present: `rm -rf models/`

### API Errors (404/Timeout)
If RMBG-2.0 API fails, the system will automatically fallback to U2-Net. Check logs:
```bash
docker-compose logs -f api
```
Look for "Falling back to U2-Net".

### Permission Errors
If you see permission errors with volumes, ensure the `uploads` directory is writable.
