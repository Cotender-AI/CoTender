"""Document endpoints. STARTER STUBS. TODO(A2): upload; TODO(A3): versions + download links."""

import uuid

from fastapi import APIRouter, Depends, File, Form, UploadFile, status

from app.core import examples as ex
from app.core.models.enums import DocumentKind, DocumentStatus
from app.core.security import ANY_MEMBER, EDITORS, Principal, require_role
from app.modules.documents.schemas import Document, DownloadLink, UploadAccepted

router = APIRouter(tags=["documents"])

_DOC = Document(
    id=ex.DOCUMENT_ID,
    tender_id=ex.TENDER_ID,
    kind=DocumentKind.tender,
    filename="RFQ-ELEC-2026-114.pdf",
    version=1,
    mime_type="application/pdf",
    file_size=2_481_920,
    page_count=24,
    checksum_sha256="0" * 64,
    processing_status=DocumentStatus.processed,
    latest_job_id=ex.JOB_ID,
    created_at=ex.NOW,
    updated_at=ex.NOW,
)


@router.post(
    "/tenders/{tender_id}/documents",
    response_model=UploadAccepted,
    status_code=status.HTTP_202_ACCEPTED,
)
def upload_document(
    tender_id: uuid.UUID,
    file: UploadFile = File(...),
    kind: DocumentKind = Form(DocumentKind.tender),
    _: Principal = Depends(require_role(*EDITORS)),
) -> UploadAccepted:
    # TODO(A2): sniff MIME from bytes, size/page caps, quota, stream to Blob with SHA-256,
    # insert document + job in one transaction, enqueue job id. No parsing here.
    doc = _DOC.model_copy(
        update={
            "tender_id": tender_id,
            "filename": file.filename or "upload",
            "kind": kind,
            "processing_status": DocumentStatus.uploaded,
        }
    )
    return UploadAccepted(document=doc, job_id=ex.JOB_ID)


@router.get("/tenders/{tender_id}/documents", response_model=list[Document])
def list_documents(
    tender_id: uuid.UUID, _: Principal = Depends(require_role(*ANY_MEMBER))
) -> list[Document]:
    return [_DOC.model_copy(update={"tender_id": tender_id})]


@router.get("/documents/{document_id}", response_model=Document)
def get_document(
    document_id: uuid.UUID, _: Principal = Depends(require_role(*ANY_MEMBER))
) -> Document:
    return _DOC.model_copy(update={"id": document_id})


@router.get("/documents/{document_id}/download", response_model=DownloadLink)
def download_document(
    document_id: uuid.UUID, _: Principal = Depends(require_role(*ANY_MEMBER))
) -> DownloadLink:
    # TODO(A3): permission check, then a 5-minute read-only SAS URL.
    return DownloadLink(url="https://example.invalid/sas-link", expires_at=ex.days(0))


@router.post(
    "/documents/{document_id}/process",
    response_model=UploadAccepted,
    status_code=status.HTTP_202_ACCEPTED,
)
def reprocess_document(
    document_id: uuid.UUID, _: Principal = Depends(require_role(*EDITORS))
) -> UploadAccepted:
    return UploadAccepted(document=_DOC.model_copy(update={"id": document_id}), job_id=ex.JOB_ID)
