
def test_creates_ticket(api_client):

    create_ticket_response = api_client.post("/create_ticket", json={
        "title": "some title",
        "description": "some description",
    })

    list_ticket_response = api_client.get("/list_tickets")

    assert create_ticket_response.status_code == 201
    assert len(list_ticket_response.json) == 1


