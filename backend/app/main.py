from fastapi import Depends, FastAPI, HTTPException, Query, Response
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text
from sqlalchemy.orm import Session

from .cache import delete_cache_pattern, get_cache, get_redis_client, set_cache
from .database import Base, engine, get_db
from .models import Movie, WatchEvent
from .schemas import HealthOut, MovieCreate, MovieOut, WatchEventCreate, WatchEventOut

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Netflix-Style Cloud Lab API",
    description="A small cloud/SRE portfolio API for catalog, playback metadata, caching, and watch events.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health", response_model=HealthOut)
def health(db: Session = Depends(get_db)):
    database_status = "ok"
    redis_status = "ok"
    try:
        db.execute(text("SELECT 1"))
    except Exception:
        database_status = "error"

    if not get_redis_client():
        redis_status = "unavailable"

    overall = "ok" if database_status == "ok" else "degraded"
    return {"status": overall, "database": database_status, "redis": redis_status}


@app.get("/movies", response_model=list[MovieOut])
def list_movies(
    response: Response,
    genre: str | None = None,
    search: str | None = None,
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
):
    cache_key = f"movies:genre={genre}:search={search}:limit={limit}"
    cached = get_cache(cache_key)
    if cached is not None:
        response.headers["X-Cache"] = "HIT"
        return cached

    query = db.query(Movie)
    if genre:
        query = query.filter(Movie.genre.ilike(f"%{genre}%"))
    if search:
        query = query.filter(Movie.title.ilike(f"%{search}%"))

    movies = query.order_by(Movie.rating.desc()).limit(limit).all()
    payload = [MovieOut.model_validate(movie).model_dump(mode="json") for movie in movies]
    set_cache(cache_key, payload)
    response.headers["X-Cache"] = "MISS"
    return payload


@app.get("/movies/{movie_id}", response_model=MovieOut)
def get_movie(movie_id: int, db: Session = Depends(get_db)):
    movie = db.query(Movie).filter(Movie.id == movie_id).first()
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    return movie


@app.post("/movies", response_model=MovieOut, status_code=201)
def create_movie(movie: MovieCreate, db: Session = Depends(get_db)):
    db_movie = Movie(**movie.model_dump())
    db.add(db_movie)
    db.commit()
    db.refresh(db_movie)
    delete_cache_pattern("movies:*")
    return db_movie


@app.post("/watch-events", response_model=WatchEventOut, status_code=201)
def create_watch_event(event: WatchEventCreate, db: Session = Depends(get_db)):
    movie = db.query(Movie).filter(Movie.id == event.movie_id).first()
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    db_event = WatchEvent(**event.model_dump())
    db.add(db_event)
    db.commit()
    db.refresh(db_event)
    return db_event


@app.get("/analytics/top-movies")
def top_movies(limit: int = Query(5, ge=1, le=20), db: Session = Depends(get_db)):
    rows = db.execute(
        text(
            """
            SELECT m.id, m.title, COUNT(w.id) AS watch_count, COALESCE(SUM(w.seconds_watched), 0) AS total_seconds
            FROM movies m
            LEFT JOIN watch_events w ON m.id = w.movie_id
            GROUP BY m.id, m.title
            ORDER BY watch_count DESC, total_seconds DESC
            LIMIT :limit
            """
        ),
        {"limit": limit},
    ).mappings().all()
    return [dict(row) for row in rows]
