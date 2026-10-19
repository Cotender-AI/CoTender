from app.core.schemas import ApiModel


class Usage(ApiModel):
    period: str
    plan: str
    documents_uploaded: int
    pages_processed: int
    monthly_page_limit: int
    exports: int
    monthly_export_limit: int
