"""Queue consumer entrypoint: `python -m app.worker`.

STARTER STUB. Block B1 replaces the idle loop with: receive a job id from the Storage Queue,
claim the job (queued -> running, skip if the idempotency key already succeeded), run the
extractor for the document's MIME type, save document_pages, record succeeded/failed with an
error_code, retry with backoff up to 3 times, then delete the queue message.
"""

import logging
import signal
import time
from types import FrameType

from app.core.config import get_settings
from app.core.logging import configure_logging

log = logging.getLogger("app.worker")
_running = True


def _stop(_signum: int, _frame: FrameType | None) -> None:
    global _running
    _running = False


def main() -> None:
    configure_logging(get_settings().log_level)
    signal.signal(signal.SIGTERM, _stop)
    signal.signal(signal.SIGINT, _stop)
    log.info("worker started (stub: no queue consumer yet, see issue B1)")
    while _running:
        time.sleep(1)  # TODO(B1): poll the queue here
    log.info("worker stopped")


if __name__ == "__main__":
    main()
