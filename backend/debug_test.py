import asyncio
import httpx
import json

async def test_api():
    async with httpx.AsyncClient(base_url="http://localhost:8000") as client:
        # Test registration
        print("Testing registration...")
        reg_response = await client.post(
            "/api/auth/register",
            json={
                "email": "test@example.com",
                "password": "password123",
                "name": "Test User"
            },
            headers={"Content-Type": "application/json"}
        )
        print(f"Registration status: {reg_response.status_code}")
        print(f"Registration response: {reg_response.text}")
        
        if reg_response.status_code == 200:
            data = reg_response.json()
            token = data['data']['token']
            user_id = data['data']['user']['id']
            
            print("\nTesting todo creation...")
            todo_response = await client.post(
                "/api/todos",
                json={
                    "title": "Test Todo",
                    "description": "This is a test todo",
                    "priority": "medium",
                    "completed": False
                },
                headers={
                    "Content-Type": "application/json",
                    "Authorization": f"Bearer {token}"
                }
            )
            print(f"Todo creation status: {todo_response.status_code}")
            print(f"Todo creation response: {todo_response.text}")

# Run the test
asyncio.run(test_api())