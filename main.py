from fastapi import FastAPI, Body
from fastapi.responses import HTMLResponse


app = FastAPI()
app.title = "Mi primera aplicación con FastAPI"
app.version = "1.0.0"

movies = [
    {
        "id": 1,
        "title": "Avatar",
        "overview": "En un exuberante planeta llamado Pandora viven los Na'vi, seres que...",
        "year": "2009",
        "rating": 7.8,
        "category": "Acción"
    },
    {
        "id": 2,
        "title": "Avatar",
        "overview": "En un exuberante planeta llamado Pandora viven los Na'vi, seres que...",
        "year": "2009",
        "rating": 7.8,
        "category": "Acción"
    }
]

@app.get("/", tags=["Home"])
def message():
    return HTMLResponse('<h1>¡Bienvenido a mi primera aplicación con FastAPI!</h1>')
    
@app.get("/movies", tags=["Movies"])
def get_movies():
    return movies

@app.get("/movies/{id}", tags=["Movies"])
def get_movie(id: int):
    for movie in movies:
        if movie["id"] == id:
            return movie
    return []

@app.get("/movies/", tags=["Movies"])
def get_movies_by_category(category: str, year: int):
    return [movie for movie in movies if movie["category"] == category ]

@app.post("/movies", tags=["Movies"])
def create_movie(id: int = Body(), title: str = Body(), overview: str = Body(), year: int = Body(), rating: float = Body(), category: str = Body()):
    movies.append({
        "id": id,
        "title": title,
        "overview": overview,
        "year": year,
        "rating": rating,
        "category": category
    })
    return movies