# SphereX Relay Server

Flask-based patch relay for SphereX automation.

## Setup for Railway

1. Push this folder to a GitHub repo
2. Connect Railway to that repo
3. It will detect:
   - `Procfile`: tells Railway how to start your server
   - `requirements.txt`: installs Flask

4. Your relay will be accessible at a public URL like:
   `https://your-app.up.railway.app`

## API Routes

- `POST /upload` (auth required)
- `GET  /latest`
- `GET  /download/<filename>`
- `POST /patch` (auth required)
- `GET  /patch.zip`

Token: `spherex-secret-token`
