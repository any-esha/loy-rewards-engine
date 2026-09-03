# Loyalty & Rewards Engine

## Start the backend

Run Uvicorn from the repository root, where `api.py` is located:

```powershell
uvicorn api:app --reload
```

The API is available at `http://localhost:8000` and its Swagger UI is at
`http://localhost:8000/docs`.

## Start the frontend

In a second terminal:

```powershell
cd frontend
npm install
npm run dev
```

Open `http://localhost:5173`. Set `VITE_API_URL` in `frontend/.env` to change the
backend URL; it defaults to `http://localhost:8000`.