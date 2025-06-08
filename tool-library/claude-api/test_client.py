#!/usr/bin/env python3
"""
Test client for Claude API
"""
import requests
import json
import time

BASE_URL = "http://localhost:8000"

def test_api():
    print("🚀 Testing Claude API...")
    
    # 1. Create a session with initial prompt
    print("\n1️⃣ Creating session...")
    response = requests.post(
        f"{BASE_URL}/sessions",
        json={
            "initial_prompt": "Hello! I'm testing the Claude API. Can you confirm you're working?",
            "session_name": "Test Session"
        }
    )
    session_data = response.json()
    session_id = session_data["session"]["id"]
    print(f"✅ Session created: {session_id}")
    print(f"Initial response: {session_data.get('initial_response', 'No response')[:100]}...")
    
    # 2. Send a follow-up message
    print("\n2️⃣ Sending follow-up message...")
    time.sleep(1)  # Small delay
    response = requests.post(
        f"{BASE_URL}/sessions/{session_id}/messages",
        json={"prompt": "Can you remember what I just said? What was my first message about?"}
    )
    message_data = response.json()
    print(f"✅ Response: {message_data['response'][:100]}...")
    
    # 3. List all sessions
    print("\n3️⃣ Listing sessions...")
    response = requests.get(f"{BASE_URL}/sessions")
    sessions = response.json()
    print(f"✅ Found {sessions['count']} sessions")
    
    # 4. Get specific session info
    print("\n4️⃣ Getting session info...")
    response = requests.get(f"{BASE_URL}/sessions/{session_id}")
    session_info = response.json()
    print(f"✅ Session name: {session_info['name']}")
    print(f"   Created: {session_info['created_at']}")
    
    # 5. Clean up
    print("\n5️⃣ Cleaning up...")
    response = requests.delete(f"{BASE_URL}/sessions/{session_id}")
    print("✅ Session deleted")
    
    print("\n✨ All tests passed!")


def interactive_test():
    """Interactive test client"""
    print("🤖 Claude API Interactive Client")
    print("Commands: 'new' for new session, 'exit' to quit")
    
    session_id = None
    
    while True:
        if session_id:
            prompt = input(f"\n[Session {session_id[:8]}]> ")
        else:
            prompt = input("\n> ")
        
        if prompt.lower() == 'exit':
            break
        elif prompt.lower() == 'new':
            # Create new session
            response = requests.post(f"{BASE_URL}/sessions", json={})
            session_id = response.json()["session"]["id"]
            print(f"Created new session: {session_id}")
            continue
        elif not session_id:
            print("No active session. Type 'new' to create one.")
            continue
        
        # Send message
        response = requests.post(
            f"{BASE_URL}/sessions/{session_id}/messages",
            json={"prompt": prompt}
        )
        
        if response.status_code == 200:
            print("\n" + response.json()["response"])
        else:
            print(f"Error: {response.text}")


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "interactive":
        interactive_test()
    else:
        test_api()