from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

async_engine: AsyncEngine | None = None
async_session_maker: async_sessionmaker[AsyncSession] | None = None


async def init_database(database_url: str) -> None:
    """
    Initialize async engine and session maker.
    """
    global async_engine, async_session_maker

    async_engine = create_async_engine(database_url, echo=False)
    async_session_maker = async_sessionmaker(
        async_engine,
        expire_on_commit=False,
    )


async def close_database() -> None:
    """
    Close database connections and dispose engine.
    """
    global async_engine, async_session_maker

    await async_engine.dispose()
    async_engine = None
    async_session_maker = None


async def get_db_session() -> AsyncSession:
    """
    Yield an async database session.
    """
    async with async_session_maker() as session:
        yield session
