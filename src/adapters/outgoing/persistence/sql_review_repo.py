from domain.port.repository.ReviewRepositoryPort import ReviewRepositoryPort
from domain.model.Review import Review as DomainReview
from domain.model.value.ImdbId import ImdbId
from adapters.outgoing.persistence.models import Movie, Review
from sqlalchemy.orm import Session

class SqlReviewRepo(ReviewRepositoryPort):
    """
    SQLAlchemy implementation of ReviewRepositoryPort.
    Assumes Movie rows exist or will be lazily inserted with minimal stub.
    """

    def __init__(self, session: Session):
        self.session = session

    def save(self, review: DomainReview) -> None:
        # ensure movie stub exists
        imdb = review.imdb_id.value
        movie_obj = self.session.get(Movie, imdb)
        if movie_obj is None:
            movie_obj = Movie(
                imdb_id = imdb,
                title   = "",      # stub; full metadata populated later
                year    = None,
                metadata= {}
            )
            self.session.add(movie_obj)

        rev = Review(
            imdb_id      = imdb,
            user_opinion = review.user_opinion.value,
            user_rating  = review.user_rating.value
        )
        self.session.add(rev)
        self.session.commit()

    def find_by_imdb(self, imdb_id: ImdbId | str) -> list[DomainReview]:
        imdb = imdb_id.value if isinstance(imdb_id, ImdbId) else imdb_id
        rows = (
            self.session
                .query(Review)
                .filter_by(imdb_id=imdb)
                .order_by(Review.created_at.desc())
                .all()
        )
        result: list[DomainReview] = []
        for row in rows:
            result.append(
                DomainReview(
                    imdb_id      = ImdbId(imdb),
                    user_opinion = row.user_opinion,
                    user_rating  = row.user_rating
                )
            )
        return result
