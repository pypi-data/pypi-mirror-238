from contextvars import ContextVar
from typing import Dict, Optional

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.types import ASGIApp

from brickworks.settings import BrickworksSettings

_SESSION: Optional[sessionmaker] = None
_session_context_var: ContextVar[Optional[AsyncSession]] = ContextVar("_session", default=None)


def get_db_url(settings: BrickworksSettings) -> str:
    if settings.DB_USE_SQLITE:
        print("WARNING! Using sqlite database. Don't do this in production please!")
        return "sqlite+aiosqlite:///sqlite.db"
    else:
        return f"postgresql+asyncpg://{settings.DB_USER}:{settings.DB_PASSWORD}@{settings.DB_HOST}/{settings.DB_NAME}"


class MissingSessionError(Exception):
    """Exception raised for when the user tries to access a database session before it is created."""

    def __init__(self):
        msg = """
        No session found! Either you are not currently in a request context,
        or you need to manually create a session context by using a `db` instance as
        a context manager e.g.:
        async with db():
            await db.session.execute(foo.select()).fetchall()
        """

        super().__init__(msg)


class SessionNotInitialisedError(Exception):
    """Exception raised when the user creates a new DB session without first initialising it."""

    def __init__(self):
        msg = """
        Session not initialised! Ensure that DBSessionMiddleware has been initialised before
        attempting database access.
        """

        super().__init__(msg)


def set_sessionmaker(settings: BrickworksSettings):
    engine_args = {}
    if not settings.DB_USE_SQLITE:
        engine_args["pool_size"] = 10
        engine_args["max_overflow"] = 20
        engine_args["pool_pre_ping"] = True

    session_args = {}
    engine = create_async_engine(get_db_url(settings), **engine_args)

    global _SESSION  # pylint: disable=global-statement
    _SESSION = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False, **session_args)  # type: ignore


class DBSessionMiddleware(BaseHTTPMiddleware):
    def __init__(self, app: ASGIApp, settings: BrickworksSettings):
        super().__init__(app)
        set_sessionmaker(settings)
        self.settings = settings

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint):
        async with db(settings=self.settings, commit_on_exit=True):
            return await call_next(request)


class DBSessionMeta(type):
    # using this metaclass means that we can access db.session as a property at a class level,
    # rather than db().session
    @property
    def session(cls) -> AsyncSession:
        """Return an instance of Session local to the current async context."""
        if _SESSION is None:
            raise SessionNotInitialisedError

        session = _session_context_var.get()
        if session is None:
            raise MissingSessionError

        return session


class DBSession(metaclass=DBSessionMeta):
    def __init__(self, settings: BrickworksSettings, session_args: Dict | None = None, commit_on_exit: bool = False):
        self.token = None
        self.session_args = session_args or {}
        self.commit_on_exit = commit_on_exit
        self.settings = settings

    async def _init_session(self):
        self.token = _session_context_var.set(_SESSION(**self.session_args))  # type: ignore

    async def __aenter__(self):
        if not isinstance(_SESSION, sessionmaker):
            set_sessionmaker(self.settings)

        await self._init_session()
        return type(self)

    async def __aexit__(self, exc_type, exc_value, traceback):
        session = _session_context_var.get()
        if not session:
            raise MissingSessionError
        if exc_type is not None:
            await session.rollback()

        if self.commit_on_exit:
            await session.commit()

        await session.close()
        _session_context_var.reset(self.token)  # type: ignore


db: DBSessionMeta = DBSession
