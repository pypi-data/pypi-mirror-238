from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker

from Bdrl import DB_URL, LOGGER

if DB_URL.startswith("postgres://"):
    url = DB_URL.replace("postgres://", "postgresql://", 1)
else:
    url = DB_URL


SPAMBOT = "SPAMBOT"


def start() -> scoped_session:
    engine = create_engine(url)
    BASE.metadata.bind = engine
    BASE.metadata.create_all(engine)
    return scoped_session(sessionmaker(bind=engine, autoflush=False))


try:
    BASE = declarative_base()
    SESSION = start()

except AttributeError as e:
    LOGGER(__name__).warning(
        "DB_URL is not configured. Features depending on the database might have issues."
    )
    LOGGER(__name__).info(str(e))

DB_AVAILABLE = False
BOTINLINE_AVAIABLE = False


def runsql() -> scoped_session:
    global DB_AVAILABLE
    engine = create_engine(url, client_encoding="utf8")
    BASE.metadata.bind = engine
    try:
        BASE.metadata.create_all(engine)
    except exc.OperationalError:
        DB_AVAILABLE = False
        return False
    DB_AVAILABLE = True
    return scoped_session(sessionmaker(bind=engine, autoflush=False))
