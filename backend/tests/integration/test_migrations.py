from sqlalchemy import Engine, inspect

from app.core.models import Base


def test_migration_creates_every_model_table(engine: Engine) -> None:
    tables = set(inspect(engine).get_table_names()) - {"alembic_version"}
    assert tables == set(Base.metadata.tables)
    assert len(tables) == 20
