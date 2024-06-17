from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from middlewares.error_handler import ErrorHandler
from routers.movie import movie_router
from routers.user import user_router

app = FastAPI()
app.title = "Mi primera aplicación con FastAPI"
app.version = "1.0.0"
app.add_middleware(ErrorHandler)
app.include_router(movie_router)
app.include_router(user_router)

@app.get("/", tags=["Home"])
def message():
    return HTMLResponse('<h1>¡Bienvenido a mi primera aplicación con FastAPI!</h1>')
    
