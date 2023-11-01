from fastapi import FastAPI
from starlette.staticfiles import StaticFiles

app = FastAPI()
app.mount("/wallaroo", StaticFiles(directory="wallaroo"))
