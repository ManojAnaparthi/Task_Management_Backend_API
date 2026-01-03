import requests
import json

BASE_URL = "http://127.0.0.1:8000"

print("=" * 60)
print("🔐 DAY 5 TEST MATRIX - Token Rotation & Security")
print("=" * 60)

# Register/Login to get initial tokens
print("\n1️⃣ Login → get tokens A1 / R1")
login_data = {"email": "testuser@example.com", "password": "testpass123"}
response = requests.post(f"{BASE_URL}/auth/login", json=login_data)

if response.status_code == 200:
    A1 = response.json()["access_token"]
    R1 = response.json()["refresh_token"]
    print(f"✅ Login successful")
    print(f"   Access Token (A1):  {A1[:30]}...")
    print(f"   Refresh Token (R1): {R1[:30]}...")
else:
    print(f"❌ Login failed: {response.status_code}")
    print("   Trying to register first...")
    register_response = requests.post(f"{BASE_URL}/auth/register", json=login_data)
    if register_response.status_code == 200:
        A1 = register_response.json()["access_token"]
        R1 = register_response.json()["refresh_token"]
        print(f"✅ Registered and got tokens")
        print(f"   Access Token (A1):  {A1[:30]}...")
        print(f"   Refresh Token (R1): {R1[:30]}...")
    else:
        print(f"❌ Register failed: {register_response.status_code} - {register_response.text}")
        exit(1)

# Test 2: Refresh using R1
print("\n2️⃣ Refresh using R1 → get A2 / R2")
refresh_response = requests.post(
    f"{BASE_URL}/auth/refresh",
    json={"refresh_token": R1}
)

if refresh_response.status_code == 200:
    A2 = refresh_response.json()["access_token"]
    R2 = refresh_response.json()["refresh_token"]
    print(f"✅ Refresh successful")
    print(f"   Access Token (A2):  {A2[:30]}...")
    print(f"   Refresh Token (R2): {R2[:30]}...")
    
    # Verify tokens are different
    if A1 != A2 and R1 != R2:
        print("   ✅ PASS: New tokens are different (rotation working)")
    else:
        print("   ⚠️  WARNING: Tokens are the same (rotation might not be working)")
else:
    print(f"❌ FAIL: Refresh failed with status {refresh_response.status_code}")
    print(f"   Response: {refresh_response.text}")
    exit(1)

# Test 3: Try refreshing with R1 again (should fail - token rotation)
print("\n3️⃣ Try refreshing again with R1 → ❌ 401 (reuse detection)")
reuse_response = requests.post(
    f"{BASE_URL}/auth/refresh",
    json={"refresh_token": R1}
)

if reuse_response.status_code == 401:
    print(f"✅ Status: {reuse_response.status_code}")
    print("   ✅ PASS: Old refresh token rejected (reuse detected)")
else:
    print(f"❌ FAIL: Expected 401, got {reuse_response.status_code}")
    print(f"   This means token rotation is not working properly!")

# Test 4: Logout using R2
print("\n4️⃣ Logout using R2")
logout_response = requests.post(
    f"{BASE_URL}/auth/logout",
    json={"refresh_token": R2}
)

if logout_response.status_code == 204:
    print(f"✅ Status: {logout_response.status_code}")
    print("   ✅ PASS: Logout successful")
else:
    print(f"❌ FAIL: Expected 204, got {logout_response.status_code}")
    print(f"   Response: {logout_response.text}")

# Test 5: Try refreshing with R2 after logout
print("\n5️⃣ Try refreshing with R2 → ❌ 401 (logout invalidation)")
post_logout_response = requests.post(
    f"{BASE_URL}/auth/refresh",
    json={"refresh_token": R2}
)

if post_logout_response.status_code == 401:
    print(f"✅ Status: {post_logout_response.status_code}")
    print("   ✅ PASS: Logged-out token rejected")
else:
    print(f"❌ FAIL: Expected 401, got {post_logout_response.status_code}")
    print(f"   Logged-out token should be invalid!")

# Test 6: Login again
print("\n6️⃣ Login again → works")
final_login = requests.post(f"{BASE_URL}/auth/login", json=login_data)

if final_login.status_code == 200:
    A3 = final_login.json()["access_token"]
    R3 = final_login.json()["refresh_token"]
    print(f"✅ Status: {final_login.status_code}")
    print(f"   Access Token (A3):  {A3[:30]}...")
    print(f"   Refresh Token (R3): {R3[:30]}...")
    print("   ✅ PASS: Can login again after logout")
else:
    print(f"❌ FAIL: Expected 200, got {final_login.status_code}")

# Summary
print("\n" + "=" * 60)
print("📊 TEST SUMMARY")
print("=" * 60)

all_passed = (
    refresh_response.status_code == 200 and
    reuse_response.status_code == 401 and
    logout_response.status_code == 204 and
    post_logout_response.status_code == 401 and
    final_login.status_code == 200
)

if all_passed:
    print("🎉 ALL TESTS PASSED!")
    print("\n✅ Token rotation working")
    print("✅ Reuse detection working")
    print("✅ Logout invalidation working")
    print("✅ Re-login working")
    print("\n🚀 DAY 5 DONE!")
else:
    print("❌ SOME TESTS FAILED")
    print("Please review the output above")

print("=" * 60)
