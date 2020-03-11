import json

import pytest

from app import crud


def test_get_voivodeship(test_app, monkeypatch):
    test_request_payload = {'lat': 52, 'lng': 16}
    test_response_payload = {'voivodeship': 'Wielkopolska'}

    async def mock_get_voivodeship(lat, lng):
        return {'name': 'Wielkopolska'}

    monkeypatch.setattr(crud, "get_voivodeship_by_point_coordinates", mock_get_voivodeship)

    response = test_app.post("/check-voiv/", data=json.dumps(test_request_payload))

    assert response.status_code == 200
    assert response.json() == test_response_payload


@pytest.mark.parametrize("event", [{"id": 0, "name": "string", "voivodeship_name": "string"}])
def test_get_event(test_app, monkeypatch, event):
    test_response_payload = event

    async def mock_get_event(event_id):
        return event

    monkeypatch.setattr(crud, "get_event", mock_get_event)
    response = test_app.get("/event/1")

    assert response.status_code == 200
    assert response.json() == test_response_payload


def test_get_event_404(test_app, monkeypatch):
    test_response_payload = {'detail': 'Event not found'}

    async def mock_get_event(event_id):
        return None

    monkeypatch.setattr(crud, "get_event", mock_get_event)
    response = test_app.get("/event/1")

    assert response.status_code == 404
    assert response.json() == test_response_payload


def test_get_events(test_app, monkeypatch):
    test_response_payload = []

    async def mock_get_events(skip, limit):
        return []

    monkeypatch.setattr(crud, "get_events", mock_get_events)
    response = test_app.get("/events/")

    assert response.status_code == 200
    assert response.json() == test_response_payload


def test_create_event(test_app, monkeypatch):
    test_request_payload = {"lng": 0, "lat": 0, "name": "string", "description": "string"}
    test_response_payload = {"id": 0, "name": "string", "voivodeship_name": "string"}

    async def mock_create_event(event):
        return {"id": 0, "name": "string", "voivodeship_name": "string"}

    monkeypatch.setattr(crud, "create_event", mock_create_event)
    response = test_app.post("/create-event/", json.dumps(test_request_payload))

    assert response.status_code == 201
    assert response.json() == test_response_payload


def test_create_event_event_outside_of_poland(test_app, monkeypatch):
    test_request_payload = {"lng": 0, "lat": 0, "name": "string", "description": "string"}
    test_response_payload = {'detail': 'Event outside of Poland'}

    async def mock_create_event(event):
        return None

    monkeypatch.setattr(crud, "create_event", mock_create_event)
    response = test_app.post("/create-event/", json.dumps(test_request_payload))

    assert response.status_code == 400
    assert response.json() == test_response_payload
