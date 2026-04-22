from fastapi import FastAPI,HTTPException
from routers import auth,notes

     
app= FastAPI()
app.include_router(auth.router)
app.include_router(notes.router)

@app.get("/")
async def root():
    return {"message": " docker World"}