
from fastapi import FastAPI, HTTPException
app = FastAPI()
#handler = Mangum(app)


@app.get("/")
async def root():
    return {"message": "Esta es mi primer server jejeje"}