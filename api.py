from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.api.routers import approvals, audit, earn, members, promotions, redeem, transactions

app = FastAPI(title="Loyalty & Rewards Engine", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:5174",
        "http://127.0.0.1:5173",
        "http://127.0.0.1:5174",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(members.router)
app.include_router(earn.router)
app.include_router(redeem.router)
app.include_router(approvals.router)
app.include_router(promotions.router)
app.include_router(transactions.router)
app.include_router(audit.router)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}