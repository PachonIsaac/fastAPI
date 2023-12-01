#http://127.0.0.1:5000/docs#/movies/get_movies_movies_get
#http://127.0.0.1:5000/docs#/
from os import path
from fastapi import FastAPI, Body, Query
from pydantic import BaseModel, Field
from fastapi.responses import HTMLResponse, JSONResponse
from typing import Optional, List
import time
#Crear una instancia de FastAPI (La aplicación)
app = FastAPI()

#Cambio en la documentación
app.title = "Mi aplicación de peliculas"
app.version = "0.0.1"

# Obtener el año actual de la fecha actual
current_year = int(time.localtime().tm_year)

class Movie(BaseModel):
    id: Optional[int] = None
    title: str = Field(..., min_length=2, max_length=50)
    overview: str = Field(..., min_length=15, max_length=50)
    year: int = Field(..., le=current_year)
    rating: float = Field(..., ge=0, le=10.0)
    category: str = Field(..., min_length=5, max_length=12)

movies = [
    {
        'id': 1,
        'title': 'Avatar',
        'overview': "En un exuberante planeta llamado Pandora viven los Na'vi, seres que ...",
        'year': '2009',
        'rating': 7.8,
        'category': 'Acción'    
    },
    {
        'id': 2,
        'title': 'Avatar',
        'overview': "En un exuberante planeta llamado Pandora viven los Na'vi, seres que ...",
        'year': '2009',
        'rating': 7.8,
        'category': 'Acción'    
    } 
]
@app.get("/", tags=["Home"], response_model=Movie, status_code=200)
def message():
    return HTMLResponse(content ="<h1>¡Mi app de peliculas!</h1>", status_code=200)

@app.get("/movies", tags=["Movies"])
def get_movies() -> List[Movie]:
    return JSONResponse(content=movies, status_code=200)

@app.get("/movies/{movie_id}", tags=["Movies"], response_model=Movie, status_code=200)
def get_movie_by_id(movie_id: int):
    # Tu lógica para obtener la película por su ID aquí
    movie = next((m for m in movies if m['id'] == movie_id), None)
    if movie:
        return JSONResponse(content=movie, status_code=200)
    else:
        return JSONResponse(content={"message": "Movie not found"}, status_code=404)

@app.get("/movies/{title}", tags=["Movies"])
def get_movie_by_title(title: str):
    movie = movies[title - 1]
    return movie

@app.get("/movies/", tags=["Movies"], response_model=Movie, status_code=200)
def get_movie_by_category(category: str = Query(min_length=5, max_length=12)):
    movie = [movie for movie in movies if movie['category'] == category]
    if len(movie) > 0:
        response = JSONResponse(content=movie, status_code=200)
    else:
        response = JSONResponse(content={"message": "Movie not found"}, status_code=404)
    return response

@app.post("/movies", tags=["Movies"], response_model=dict, status_code=201)
def create_movie(movie: Movie):
    movies.append(movie)
    return JSONResponse(content={"message": "Movie created successfully"}, status_code=201)

@app.put("/movies/{movie_id}", tags=["Movies"], response_model=dict)
def update_movie(movie:Movie):
    for movie in movies:
        if movie['id'] == movie.movie_id:
            movie.title = movie.title
            movie['overview'] = movie.overview
            movie['year'] = movie.year
            movie['rating'] = movie.rating
            movie['category'] = movie.category
    return JSONResponse(content={"message": "Movie updated successfully"}, status_code=200)

@app.delete("/movies/{movie_id}", tags=["Movies"], response_model=dict)
def delete_movie(movie_id: int):
    for movie in movies:
        if movie['id'] == movie_id:
            movies.remove(movie)
    return JSONResponse(content={"message": "Movie deleted successfully"}, status_code=200)