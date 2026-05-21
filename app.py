from fastapi import FastAPI
from backend.api.routes import router

app = FastAPI(title="Neurosymbolic Restaurant Agent API")
app.include_router(router, prefix="/api")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
