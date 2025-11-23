import pytest
from fastapi.testclient import TestClient
from src.api.main import app

@pytest.mark.asyncio
async def test_automation_api_response():
    client = TestClient(app)

    try:
        # Test request
        request_data = {
            "user_query": "Find the cheapest jeans for men and add to the cart."
        }

        # Make API call
        response = client.post("/api/run-automation", json=request_data)

        # Print the response
        print("API Response Status:", response.status_code)
        print("API Response Body:", response.json())

        # Simple assertion
        assert response.status_code == 200

    except Exception as e:
        print(f"Test failed with error: {e}")
        assert False, f"API call failed: {str(e)}"