"""Base class for every tenant-owned repository (CLAUDE.md rule 2, BR-05).

All SQL lives in repositories. Every select/update/delete built here is filtered by the
organisation_id taken from the verified token, so another organisation's row is simply
"not found" (404), never "forbidden".
"""

import uuid
from typing import Any, ClassVar

from sqlalchemy import Select, delete, func, select, update
from sqlalchemy.orm import Session

from app.core.errors import NotFoundError
from app.core.models import Base


class OrgScopedRepository[ModelT: Base]:
    model: ClassVar[type[Any]]

    def __init_subclass__(cls, **kwargs: Any) -> None:
        super().__init_subclass__(**kwargs)
        model = cls.__dict__.get("model")
        if model is not None and not hasattr(model, "organisation_id"):
            raise TypeError(f"{model.__name__} has no organisation_id; it cannot be org-scoped")

    def __init__(self, session: Session, organisation_id: uuid.UUID) -> None:
        self.session = session
        self.organisation_id = organisation_id

    # -- building blocks for subclasses: always start from these, never from select(model)
    def _select(self) -> Select[tuple[ModelT]]:
        return select(self.model).where(self.model.organisation_id == self.organisation_id)

    # -- generic operations
    def get(self, id_: uuid.UUID) -> ModelT | None:
        return self.session.scalars(self._select().where(self.model.id == id_)).first()

    def get_or_404(self, id_: uuid.UUID) -> ModelT:
        obj = self.get(id_)
        if obj is None:
            raise NotFoundError(f"{self.model.__tablename__} not found", {"id": str(id_)})
        return obj

    def list(
        self, *where: Any, order_by: Any = None, limit: int = 100, offset: int = 0
    ) -> list[ModelT]:
        stmt = self._select().where(*where).limit(limit).offset(offset)
        if order_by is not None:
            stmt = stmt.order_by(order_by)
        return list(self.session.scalars(stmt))

    def count(self, *where: Any) -> int:
        stmt = (
            select(func.count())
            .select_from(self.model)
            .where(self.model.organisation_id == self.organisation_id, *where)
        )
        return int(self.session.scalar(stmt) or 0)

    def add(self, obj: ModelT) -> ModelT:
        current = getattr(obj, "organisation_id", None)
        if current is not None and current != self.organisation_id:
            raise ValueError("refusing to write a row for another organisation")
        obj.organisation_id = self.organisation_id  # type: ignore[attr-defined]
        self.session.add(obj)
        self.session.flush()
        return obj

    def update(self, id_: uuid.UUID, **values: Any) -> int:
        values.pop("organisation_id", None)  # moving rows between orgs is never allowed
        stmt = (
            update(self.model)
            .where(self.model.organisation_id == self.organisation_id, self.model.id == id_)
            .values(**values)
        )
        return self.session.execute(stmt).rowcount  # type: ignore[attr-defined, no-any-return]

    def delete(self, id_: uuid.UUID) -> int:
        stmt = delete(self.model).where(
            self.model.organisation_id == self.organisation_id, self.model.id == id_
        )
        return self.session.execute(stmt).rowcount  # type: ignore[attr-defined, no-any-return]
