from app.database import Base, SessionLocal, engine
from app.models import Movie

Base.metadata.create_all(bind=engine)

MOVIES = [
    {
        "title": "Cloudfall",
        "genre": "Sci-Fi",
        "description": "A systems engineer races to keep a global streaming platform online during a massive outage.",
        "release_year": 2026,
        "rating": 8.7,
        "thumbnail_url": "https://picsum.photos/seed/cloudfall/500/300",
        "video_url": "https://example.com/videos/cloudfall.mp4",
    },
    {
        "title": "The Last Deploy",
        "genre": "Drama",
        "description": "A junior cloud engineer learns the hard way why production changes need rollbacks.",
        "release_year": 2025,
        "rating": 8.3,
        "thumbnail_url": "https://picsum.photos/seed/deploy/500/300",
        "video_url": "https://example.com/videos/last-deploy.mp4",
    },
    {
        "title": "Cache Me If You Can",
        "genre": "Action",
        "description": "A high-traffic API survives Black Friday through Redis caching and smart architecture.",
        "release_year": 2024,
        "rating": 8.9,
        "thumbnail_url": "https://picsum.photos/seed/cache/500/300",
        "video_url": "https://example.com/videos/cache-me.mp4",
    },
    {
        "title": "Region Failover",
        "genre": "Thriller",
        "description": "When one region goes down, a team must fail over before users notice.",
        "release_year": 2023,
        "rating": 8.1,
        "thumbnail_url": "https://picsum.photos/seed/failover/500/300",
        "video_url": "https://example.com/videos/failover.mp4",
    },
]


def main():
    db = SessionLocal()
    try:
        for movie in MOVIES:
            exists = db.query(Movie).filter(Movie.title == movie["title"]).first()
            if not exists:
                db.add(Movie(**movie))
        db.commit()
        print("Seeded database.")
    finally:
        db.close()


if __name__ == "__main__":
    main()
