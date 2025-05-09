from fastapi import FastAPI
from .database.config import engine, Base
from .routes.auth_route import router as auth_router
from .routes.admin_route import router as admin_router
from .routes.user_route import router as user_router
app = FastAPI()

Base.metadata.create_all(bind=engine)
Base.metadata.create_all(bind=engine)

@app.get("/")
def home():
    return {"hello":"world"}

app.include_router(auth_router, prefix="/api/auth")
app.include_router(admin_router, prefix="/api/admin")
app.include_router(user_router, prefix="/api/user")
