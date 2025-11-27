def test_health(client):
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json()["database"] == "ok"

def test_list_job_boards(client):
    response = client.get("/api/job-boards")
    assert response.status_code == 200
    assert response.json() == []

import os
import file_storage
from config import settings

def test_create_job_board(client, monkeypatch):
    monkeypatch.setattr(settings, "ADMIN_USERNAME", "admin")
    monkeypatch.setattr(settings, "ADMIN_PASSWORD", "test")
    login_data = {"username": "admin", "password": "test"}
    login_response = client.post("/api/admin-login", data=login_data)
    assert login_response.status_code == 200

    def mock_upload_file(bucket_name, path, contents, content_type):
        return "test/logo.png"
    monkeypatch.setattr(file_storage, "upload_file", mock_upload_file)

    files_payload = {
          "logo": ("logo.png", b"some file")
    }
    response = client.post("/api/job-boards", files=files_payload, data={"slug": "acme"})
    assert response.status_code == 200
    new_job_board = response.json()
    assert  new_job_board['slug'] == "acme"
    assert  new_job_board['logo_url'] == "test/logo.png"

