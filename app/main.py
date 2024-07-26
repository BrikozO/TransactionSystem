import uvicorn
from fastapi import FastAPI

from app.routers import user, admin, auth, transactions_webhook

app = FastAPI()
app.include_router(user.router)
app.include_router(admin.router)
app.include_router(auth.router)
app.include_router(transactions_webhook.router)

if __name__ == '__main__':
    uvicorn.run('app.main:app', reload=True)
