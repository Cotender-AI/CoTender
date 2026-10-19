from fastapi.testclient import TestClient


def test_health(client: TestClient) -> None:
    res = client.get("/health")
    assert res.status_code == 200
    assert res.json() == {"status": "ok"}


def test_unknown_route_uses_standard_error_format(client: TestClient) -> None:
    res = client.get("/api/v1/does-not-exist")
    assert res.status_code == 404
    assert res.json()["error"]["code"] == "not_found"


def test_validation_error_uses_standard_error_format(client: TestClient) -> None:
    res = client.post("/api/v1/tenders", json={"title": ""})
    assert res.status_code == 422
    body = res.json()["error"]
    assert body["code"] == "validation_error"
    assert body["details"]["errors"]


def test_money_is_serialised_as_strings(client: TestClient) -> None:
    totals = client.get(f"/api/v1/tenders/{'0' * 8}-0000-4000-8000-000000000201/boq").json()
    assert isinstance(totals["totals"]["total"], str)
