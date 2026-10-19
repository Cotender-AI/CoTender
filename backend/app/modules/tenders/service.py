"""Business rules for tenders. TODO(C1): create, update with allowed status transitions only
(invalid -> InvalidTransitionError / 422), archive, dashboard. Record audit events.
Routers call one service method; services never build SQL (use TenderRepository)."""
