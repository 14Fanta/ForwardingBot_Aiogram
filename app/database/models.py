from sqlalchemy import BigInteger,String
from sqlalchemy.orm import Mapped, mapped_column,DeclarativeBase
from sqlalchemy.ext.asyncio import AsyncAttrs,create_async_engine,async_sessionmaker

engine = create_async_engine(url='sqlite+aiosqlite:///db.sqlite3',echo= True)
async_session = async_sessionmaker(engine)

class Base(DeclarativeBase,AsyncAttrs):
    pass

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    tg_id: Mapped[int] = mapped_column(BigInteger, nullable=True)
    full_name: Mapped[str] = mapped_column(String(225), nullable=True)
    group: Mapped[str] = mapped_column(String(225), nullable=True)

async def async_main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)