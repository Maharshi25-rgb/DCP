from fastapi import FastAPI

from routers.message import router as message_router
from routers.workflow import router as workflow_router


app = FastAPI(
    title="DCP API",
    description=(
        "Dynamic Context Processing - "
        "Generic AI Workflow Engine"
    ),
    version="0.1.0"
)


@app.get("/")
def home():

    return {
        "message": "Welcome to DCP",
        "status": "running"
    }


@app.get("/about")
def about():

    return {
        "message": "This is the DCP backend",
        "version": "0.1.0"
    }


@app.get("/health")
def health_check():

    return {
        "status": "healthy"
    }


app.include_router(message_router)

app.include_router(workflow_router)