import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_health_check(async_client: AsyncClient):
    response = await async_client.get("/api/v1/health")
    assert response.status_code == 200
    data = response.json()
    assert "status" in data
    assert "database" in data
    assert "llm_providers" in data

@pytest.mark.asyncio
async def test_session_lifecycle(async_client: AsyncClient):
    # 1. Create Session
    create_res = await async_client.post("/api/v1/sessions", json={"title": "Test Growth Session", "provider": "ollama"})
    assert create_res.status_code == 201
    session_data = create_res.json()
    session_id = session_data["id"]
    assert session_data["title"] == "Test Growth Session"

    # 2. List Sessions
    list_res = await async_client.get("/api/v1/sessions")
    assert list_res.status_code == 200
    sessions = list_res.json()
    assert len(sessions) >= 1

    # 3. Get Session details
    get_res = await async_client.get(f"/api/v1/sessions/{session_id}")
    assert get_res.status_code == 200
    assert get_res.json()["id"] == session_id

    # 4. Delete Session
    del_res = await async_client.delete(f"/api/v1/sessions/{session_id}")
    assert del_res.status_code == 204

@pytest.mark.asyncio
async def test_providers_toggle(async_client: AsyncClient):
    get_res = await async_client.get("/api/v1/providers")
    assert get_res.status_code == 200

    toggle_res = await async_client.post("/api/v1/providers/toggle", json={"provider": "anthropic"})
    assert toggle_res.status_code == 200
    assert toggle_res.json()["current_provider"] == "anthropic"
