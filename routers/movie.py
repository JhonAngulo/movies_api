from fastapi import APIRouter, Depends, Path, Query
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from typing import Optional, List
from config.database import Session
from models.movie import Movie as MovieModel
from fastapi.encoders import jsonable_encoder
from middlewares.jwt_bearer import JWTBearer
from services.movie import MovieService
from schemas.movie import Movie

movie_router = APIRouter()

@movie_router.get("/movies", tags=["Movies"], response_model=List[Movie], status_code=200, dependencies=[Depends(JWTBearer())])
def get_movies() -> List[Movie]:
    db = Session()
    result = MovieService(db).get_movies()
    return JSONResponse(content=jsonable_encoder(result), status_code=200)

@movie_router.get("/movies/{id}", tags=["Movies"], response_model=Movie, status_code=200)
def get_movie(id: int = Path(ge=1, le=2000)) -> Movie:
    db = Session()
    result = MovieService(db).get_movie(id)
    if not result:
        return JSONResponse(content={'message': 'without results'}, status_code=404)
    return JSONResponse(content=jsonable_encoder(result), status_code=200)

    # for movie in movies:
    #     if movie["id"] == id:
    #         return JSONResponse(content=movie, status_code=200)
    # return JSONResponse(content=[], status_code=404)

@movie_router.get("/movies/", tags=["Movies"], response_model=List[Movie])
def get_movies_by_category(category: str = Query(min_length=5, max_length=15)) -> List[Movie]:
    db = Session()
    result = MovieService(db).get_movies_by_category(category)
    if not result:
        return JSONResponse(content={'message': 'without results'}, status_code=404)
    return JSONResponse(content=jsonable_encoder(result), status_code=200)

    # data = [movie for movie in movies if movie["category"] == category]
    # return JSONResponse(content=data)

@movie_router.post("/movies", tags=["Movies"], response_model=dict, status_code=201)
def create_movie(movie: Movie) -> dict:
    db = Session()
    MovieService(db).create_movie(movie)
    return JSONResponse(content={"message": "Movie created successfully"}, status_code=201)


@movie_router.put("/movies/{id}", tags=["Movies"], response_model=dict, status_code=200)
def update_movie(id: int, movie: Movie) -> dict:
    db = Session()
    result = MovieService(db).update_movie(id, movie)
    if not result:
        return JSONResponse(content={"message": "Movie not found"}, status_code=404)
    return JSONResponse(content={"message": "Movie updated successfully"}, status_code=200)

    # for item in movies:
    #     if item["id"] == id:
    #         item["title"] = movie.title
    #         item["overview"] = movie.overview
    #         item["year"] = movie.year
    #         item["rating"] = movie.rating
    #         item["category"] = movie.category
    #         return JSONResponse(content={"message": "Movie updated successfully"}, status_code=200)
    # return JSONResponse(content={"message": "Movie not found"}, status_code=404)


@movie_router.delete("/movies/{id}", tags=["Movies"], response_model=dict, status_code=200)
def delete_movie(id: int) -> dict:
    db = Session()
    result = MovieService(db).delete_movie(id)
    if not result:
        return JSONResponse(content={"message": "Movie not found"}, status_code=404)
    return JSONResponse(content={"message": "Movie deleted successfully"}, status_code=200)
    # for movie in movies:
    #     if movie["id"] == id:
    #         movies.remove(movie)
    #         return JSONResponse(content={"message": "Movie deleted successfully"}, status_code=200)
    #     return JSONResponse(content={"message": "Movie not found"}, status_code=404)