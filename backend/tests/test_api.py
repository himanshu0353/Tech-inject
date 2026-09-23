import pytest
from fastapi.testclient import TestClient
from backend.app.main import app

def test_health_check():
    with TestClient(app) as client:
        response = client.get("/api/health")
        assert response.status_code == 200
        assert response.json()["status"] == "ok"

def test_list_published_components():
    with TestClient(app) as client:
        response = client.get("/api/components")
        assert response.status_code == 200
        components = response.json()
        assert len(components) >= 10
        for c in components:
            assert c["status"] == "published"

def test_free_component_detail():
    with TestClient(app) as client:
        response = client.get("/api/components/button")
        assert response.status_code == 200
        data = response.json()
        assert data["slug"] == "button"
        assert data["is_locked"] is False
        assert data["source_files"] is not None
        assert "Button.tsx" in data["source_files"]

def test_premium_component_locked_for_signed_out():
    with TestClient(app) as client:
        response = client.get("/api/components/data-table")
        assert response.status_code == 200
        data = response.json()
        assert data["slug"] == "data-table"
        assert data["is_locked"] is True
        assert data["source_files"] is None  # Source code must NOT leak!

def test_auth_login():
    with TestClient(app) as client:
        response = client.post("/api/auth/login", json={"email": "free@example.com", "password": "customer123"})
        assert response.status_code == 200
        user_data = response.json()
        assert user_data["email"] == "free@example.com"
        assert user_data["is_premium"] is False

def test_auth_signup():
    import uuid
    email = f"user_{uuid.uuid4().hex[:8]}@example.com"
    with TestClient(app) as client:
        response = client.post("/api/auth/signup", json={"email": email, "password": "password123"})
        assert response.status_code == 200
        user_data = response.json()
        assert user_data["email"] == email
        assert user_data["role"] == "customer"
        assert user_data["is_premium"] is False

def test_admin_create_and_delete_component():
    with TestClient(app) as client:
        # Login as admin
        login_res = client.post("/api/auth/login", json={"email": "admin@techinject.com", "password": "admin123"})
        assert login_res.status_code == 200

        # Create component
        create_res = client.post("/api/admin/components", json={
            "slug": "test-widget",
            "name": "Test Widget",
            "description": "Temporary test widget",
            "category": "Actions",
            "access_level": "free",
            "version": "1.0.0",
            "props": [],
            "dependencies": [],
            "preview_data": {},
            "source_files": {"TestWidget.tsx": "export const TestWidget = () => null;"}
        })
        assert create_res.status_code == 200
        comp_id = create_res.json()["id"]

        # Delete component
        delete_res = client.delete(f"/api/admin/components/{comp_id}")
        assert delete_res.status_code == 200
        assert "deleted successfully" in delete_res.json()["message"]

