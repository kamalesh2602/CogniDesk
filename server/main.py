from fastapi import FastAPI

print("HELLO FROM MAIN")

app = FastAPI()

@app.get("/")
def root():
    return {"status": "ok"}