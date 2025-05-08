from fastapi import FastAPI
from .models.user_model import Base
from .database.db_config import engine
from .routes.user_route import router as user_router
from .routes.admin_route import router as admin_router
app = FastAPI()

Base.metadata.create_all(bind=engine)

@app.get("/")
def home():
    return {"hello":"world"}

app.include_router(user_router, prefix="/api/user")
app.include_router(admin_router, prefix="/api/admin")
