import requests
import sys

BASE_URL = "http://127.0.0.1:8000"

def check_url(path, expected_status=200, allow_redirects=True):
    url = f"{BASE_URL}{path}"
    try:
        response = requests.get(url, allow_redirects=allow_redirects)
        print(f"Checking {path}: Status {response.status_code}", end=" ")
        if response.status_code == expected_status:
            print("✅")
            return True
        elif allow_redirects and response.history:
            print(f" (Redirected to {response.url})", end=" ")
            if response.status_code == 200: # Eventually 200
                 print("✅ (via redirect)")
                 return True
        
        print(f"❌ (Expected {expected_status})")
        return False
    except Exception as e:
        print(f"Checking {path}: Error connecting ❌ - {e}")
        return False

def run_checks():
    print("--- RoomLink Route Verification ---")
    
    # Public Pages
    check_url("/")
    check_url("/houses/")
    check_url("/roommates/")
    
    # Auth Pages
    check_url("/login/")
    check_url("/signup/")
    
    # Protected Pages (Should redirect to login)
    # requests.get follows redirects by default, so we expect 200 (login page) 
    # but we can check history to see if it redirected
    print("\n--- Access Control Verification ---")
    
    # Profile should redirect to login
    r = requests.get(f"{BASE_URL}/profile/", allow_redirects=False)
    if r.status_code == 302 and "/login" in r.headers.get('Location', ''):
        print(f"Checking /profile/ (Unauthenticated): Redirects to Login ✅")
    else:
        print(f"Checking /profile/ (Unauthenticated): Status {r.status_code} ❌")

    # Post Listing should redirect to login
    r = requests.get(f"{BASE_URL}/post/", allow_redirects=False)
    if r.status_code == 302 and "/login" in r.headers.get('Location', ''):
        print(f"Checking /post/ (Unauthenticated): Redirects to Login ✅")
    else:
        print(f"Checking /post/ (Unauthenticated): Status {r.status_code} ❌")

if __name__ == "__main__":
    run_checks()
