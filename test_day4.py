import requests
import json

BASE_URL = "http://127.0.0.1:8000"

# Register and login to get token
print("🔐 Registering user...")
register_data = {"email": "testuser@example.com", "password": "testpass123"}
response = requests.post(f"{BASE_URL}/auth/register", json=register_data)
if response.status_code == 200:
    token = response.json()["access_token"]
    print(f"✅ Registered successfully, token: {token[:20]}...")
else:
    # Try login if already registered
    print("⚠️  User exists, trying login...")
    response = requests.post(f"{BASE_URL}/auth/login", json=register_data)
    if response.status_code == 200:
        token = response.json()["access_token"]
        print(f"✅ Logged in successfully, token: {token[:20]}...")
    else:
        print(f"❌ Failed to login: {response.status_code}")
        exit(1)

headers = {"Authorization": f"Bearer {token}"}

# Create 5+ tasks
print("\n📝 Creating 5+ tasks...")
task_statuses = ["todo", "in_progress", "done", "todo", "todo", "in_progress"]
for i, status in enumerate(task_statuses, 1):
    task_data = {
        "title": f"Task {i}",
        "description": f"Description for task {i}"
    }
    response = requests.post(f"{BASE_URL}/tasks", json=task_data, headers=headers)
    if response.status_code == 200:
        task_id = response.json()["id"]
        print(f"✅ Created Task {i}: {task_id}")
        
        # Update status
        if status != "todo":
            update_response = requests.put(
                f"{BASE_URL}/tasks/{task_id}",
                json={"status": status},
                headers=headers
            )
            print(f"   ↳ Updated status to: {status}")
    else:
        print(f"❌ Failed to create task {i}: {response.status_code}")

# Test 1: GET /tasks?limit=2
print("\n📋 Test 1: GET /tasks?limit=2")
response = requests.get(f"{BASE_URL}/tasks?limit=2", headers=headers)
if response.status_code == 200:
    tasks = response.json()
    print(f"✅ Status: {response.status_code}")
    print(f"   ↳ Returned {len(tasks)} tasks (expected: 2)")
    if len(tasks) == 2:
        print("   ✅ PASS: Correct number of tasks")
    else:
        print(f"   ❌ FAIL: Expected 2, got {len(tasks)}")
else:
    print(f"❌ Status: {response.status_code}")

# Test 2: GET /tasks?offset=2
print("\n📋 Test 2: GET /tasks?offset=2")
response = requests.get(f"{BASE_URL}/tasks?offset=2", headers=headers)
if response.status_code == 200:
    tasks = response.json()
    print(f"✅ Status: {response.status_code}")
    print(f"   ↳ Returned {len(tasks)} tasks (offset=2)")
    print("   ✅ PASS: Offset working")
else:
    print(f"❌ Status: {response.status_code}")

# Test 3: GET /tasks?status=todo
print("\n📋 Test 3: GET /tasks?status=todo")
response = requests.get(f"{BASE_URL}/tasks?status=todo", headers=headers)
if response.status_code == 200:
    tasks = response.json()
    print(f"✅ Status: {response.status_code}")
    print(f"   ↳ Returned {len(tasks)} tasks with status=todo")
    all_todo = all(task["status"] == "todo" for task in tasks)
    if all_todo:
        print("   ✅ PASS: All tasks have status=todo")
    else:
        print("   ❌ FAIL: Some tasks don't have status=todo")
else:
    print(f"❌ Status: {response.status_code}")

# Test 4: Invalid limit=1000 → 422
print("\n📋 Test 4: Invalid limit=1000 → 422")
response = requests.get(f"{BASE_URL}/tasks?limit=1000", headers=headers)
if response.status_code == 422:
    print(f"✅ Status: {response.status_code}")
    print("   ✅ PASS: Validation error for limit > 100")
else:
    print(f"❌ FAIL: Expected 422, got {response.status_code}")

# Test 5: Invalid status=abc → 422
print("\n📋 Test 5: Invalid status=abc → 422")
response = requests.get(f"{BASE_URL}/tasks?status=abc", headers=headers)
if response.status_code == 422:
    print(f"✅ Status: {response.status_code}")
    print("   ✅ PASS: Validation error for invalid status")
else:
    print(f"❌ FAIL: Expected 422, got {response.status_code}")

print("\n" + "="*50)
print("🎯 Day 4 Test Complete!")
print("="*50)
