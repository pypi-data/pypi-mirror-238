def test_view(client):
    response = client.get("/")
    assert "<title>SWH GraphQL explorer</title>" in response.text
    assert "login</a>" in response.text
    assert "<span>Software Heritage GraphQL Explorer</span>" in response.text
