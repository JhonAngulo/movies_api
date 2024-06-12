from fastapi import FastAPI, Body, Path, Query
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel, Field
from typing import Optional, List


app = FastAPI()
app.title = "Mi primera aplicación con FastAPI"
app.version = "1.0.0"


class Movie(BaseModel):
    id: Optional[int] = None
    title: str = Field(min_length=5, max_length=30)
    overview: str = Field(min_length=15, max_length=100)
    year: int = Field(le=2022)
    rating: float = Field(ge=1, le=10)
    category: str  = Field(min_length=5, max_length=15)

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "id": 3,
                    "title": "Título de la película",
                    "overview": "Descripción de la película...",
                    "year": "2022",
                    "rating": 9.8,
                    "category": "Humor"
                }
            ]
        }
    }

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
    
@app.get("/movies", tags=["Movies"], response_model=List[Movie], status_code=200)
def get_movies() -> List[Movie]:
    return JSONResponse(content=movies, status_code=200)

@app.get("/movies/{id}", tags=["Movies"], response_model=Movie, status_code=200)
def get_movie(id: int = Path(ge=1, le=2000)) -> Movie:
    for movie in movies:
        if movie["id"] == id:
            return JSONResponse(content=movie, status_code=200)
    return JSONResponse(content=[], status_code=404)

@app.get("/movies/", tags=["Movies"], response_model=List[Movie])
def get_movies_by_category(category: str = Query(min_length=5, max_length=15)) -> List[Movie]:
    data = [movie for movie in movies if movie["category"] == category]
    return JSONResponse(content=data)

@app.post("/movies", tags=["Movies"], response_model=dict, status_code=201)
def create_movie(movie: Movie) -> dict:
    movies.append(movie)
    return JSONResponse(content={"message": "Movie created successfully"}, status_code=201)


@app.put("/movies/{id}", tags=["Movies"], response_model=dict, status_code=200)
def update_movie(id: int, movie: Movie) -> dict:
    for item in movies:
        if item["id"] == id:
            item["title"] = movie.title
            item["overview"] = movie.overview
            item["year"] = movie.year
            item["rating"] = movie.rating
            item["category"] = movie.category
            return JSONResponse(content={"message": "Movie updated successfully"}, status_code=200)
    return JSONResponse(content={"message": "Movie not found"}, status_code=404)


@app.delete("/movies/{id}", tags=["Movies"], response_model=dict, status_code=200)
def delete_movie(id: int) -> dict:
    for movie in movies:
        if movie["id"] == id:
            movies.remove(movie)
            return JSONResponse(content={"message": "Movie deleted successfully"}, status_code=200)
        return JSONResponse(content={"message": "Movie not found"}, status_code=404)