from fastapi import FastAPI

app = FastAPI()

# Root and Health Check
@app.get("/")
def root():
    return {"message": "Voia is LIVE!🚀"}

@app.get("/healthz")
async def health_check():
    return {"status": "ok"}
