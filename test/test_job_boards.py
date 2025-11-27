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
    monkeypatch.setattr(settings, "ADMIN_PASSWORD", "secret")
    login_data = {"username": "admin", "password": "secret"}
    login_response = client.post("/api/admin-login", data=login_data)
    assert login_response.status_code == 200

    mock_return_value = "test/logo.txt"
    def mock_fetch_external_data(bucket_name, path, contents, content_type):
        return mock_return_value
    monkeypatch.setattr(file_storage, "upload_file", mock_fetch_external_data)

    files_payload = {
          "logo": ("logo.txt", b"some file", "text/plain")
    }
    response = client.post("/api/job-boards", files=files_payload, data={"slug": "acme"})
    assert response.status_code == 200
    new_job_board = response.json()
    assert  new_job_board['slug'] == "acme"
    assert  new_job_board['logo_url'] == "/uploads/company-logos/logo.txt"

