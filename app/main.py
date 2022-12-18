from fastapi import FastAPI

app = FastAPI()


@app.post('/productionplan/')
def productionplan():
    return {'hel': 'lo'}
