from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import engine, Base
from .routers import auth, components, admin, customers
from .seed import seed_database

@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    seed_database()
    yield

app = FastAPI(
    title="Tech Inject Design Library API",
    description="Backend services for component registry, auth, dynamic publishing, and installer CLI",
    version="1.0.0",
    lifespan=lifespan
)

# Enable CORS for React Frontend (running on localhost:5173 or localhost:3000)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(components.router)
app.include_router(admin.router)
app.include_router(customers.router)

@app.get("/api/health")
def health_check():
    return {"status": "ok", "service": "Tech Inject FastAPI"}
