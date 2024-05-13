import logging

from sqlalchemy import Engine
from sqlmodel import Session, select
from tenacity import retry, before_log, after_log, wait_fixed, stop_after_attempt

from app.core.database import engine, init_db

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

max_tries = 300  # 5 mins
wait_time = 1  # time in sec


@retry(
    stop=stop_after_attempt(max_tries),
    wait=wait_fixed(wait_time),
    before=before_log(logger, logging.INFO),
    after=after_log(logger, logging.WARN),
)
def init(db_engine: Engine) -> None:
    try:
        with Session(db_engine) as session:
            # Try to create session to check if DB is awake
            session.exec(select(1))
    except Exception as e:
        logger.error(e)
        raise e


def init_db_tbl() -> None:
    with Session(engine) as session:
        init_db(session)


def main() -> None:
    logger.info("Initializing service")
    init(engine)
    init_db_tbl()
    logger.info("Service finished initializing")


if __name__ == "__main__":
    main()
