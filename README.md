# Jeb Incubator Platform

A full-stack web application for managing startups, partners, and users. Built with FastAPI (backend) and React + Vite (frontend).

## Prerequisites

- [Nix](https://nixos.org/download.html) (recommended for reproducible dev environment)

## Quickstart (Recommended: Nix)

1. **Clone the repository**

   ```sh
   git clone <https://github.com/Sigmapitech/survivor_pool>
   cd survivor_pool
   ```

2. **Enter Nix shell**

   ```sh
   nix develop
   ```

3. **Set up environment variables**
   - Create `.env.dev` or `.env.prod` and adjust values as needed.`lo
   - `log level` (optional)
   - `jeb api url`
   - `jeb_api_auth` token of the API
   - `jwt_secret` jwt token secret encryption
   - `mail_user`
   - `mail_pass`

4. **Run the frontend (React + Vite)**

   ```sh
   npm install --prefix front
   npm run dev --prefix front
   ```

   The frontend will be available at [http://localhost:5173](http://localhost:5173).

5. **Run the backend (FastAPI)**

   ```sh
   fastapi dev
   ```

## Deployment

- Set up production environment variables (`.env.prod`).
- Build frontend for production:

  ```sh
  cd front
  npm run build
  ```

- Serve the frontend build with a static server or reverse proxy.
- Run backend with a production ASGI server (e.g., Uvicorn or Gunicorn).

## Project Structure

- `app` — FastAPI backend
- `front` — React frontend
- `tests` — Backend tests
- `nix` — Nix configuration
- `.env*` — Environment variables

---

For troubleshooting or more details, see individual module documentation or contact the maintainers.
