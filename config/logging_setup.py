import logging
import sys


def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[
            logging.StreamHandler(sys.stdout)  # This ensures logs go to stdout
        ]
    )

    logging.getLogger("sqlalchemy.engine").setLevel(logging.ERROR)
    logging.getLogger("alembic").setLevel(logging.WARNING)
