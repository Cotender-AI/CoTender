"""Exports. STARTER STUBS. TODO(C5): Excel; TODO(C5-PDF): checklist PDF."""

import uuid

from fastapi import APIRouter, Depends, status

from app.core import examples as ex
from app.core.models.enums import ExportKind, Role
from app.core.security import ANY_MEMBER, EDITORS, Principal, require_role
from app.modules.documents.schemas import DownloadLink
from app.modules.exports.schemas import Export, ExportCreate

router = APIRouter(tags=["exports"])
EXPORTERS = (*EDITORS, Role.project_manager)

_EXPORT = Export(
    id=ex.uid(7001),
    tender_id=ex.TENDER_ID,
    kind=ExportKind.boq_excel,
    version=1,
    is_draft=True,
    generated_at=ex.NOW,
    generated_by_name="Demo Estimator",
)


@router.post(
    "/tenders/{tender_id}/exports", response_model=Export, status_code=status.HTTP_201_CREATED
)
def create_export(
    tender_id: uuid.UUID, body: ExportCreate, _: Principal = Depends(require_role(*EXPORTERS))
) -> Export:
    return _EXPORT.model_copy(
        update={"tender_id": tender_id, "kind": body.kind, "is_draft": body.draft}
    )


@router.get("/tenders/{tender_id}/exports", response_model=list[Export])
def list_exports(
    tender_id: uuid.UUID, _: Principal = Depends(require_role(*ANY_MEMBER))
) -> list[Export]:
    return [_EXPORT]


@router.get("/exports/{export_id}/download", response_model=DownloadLink)
def download_export(
    export_id: uuid.UUID, _: Principal = Depends(require_role(*ANY_MEMBER))
) -> DownloadLink:
    return DownloadLink(url="https://example.invalid/sas-link", expires_at=ex.days(0))
