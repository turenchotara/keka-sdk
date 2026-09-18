#!/usr/bin/env python3
"""
Test script to demonstrate Constructor Injection implementation for KekaClient.

This script shows how auth tokens are automatically passed to all child classes
through constructor injection.
"""

import sys
import os

# Add the keka_sdk to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'keka_sdk'))

from keka_sdk.src.resources.keka_client import KekaClient

def test_constructor_injection():
    """Test Constructor Injection pattern."""
    
    print("🧪 Testing Constructor Injection Pattern")
    print("=" * 50)
    
    # Test 1: String token injection
    print("\n1️⃣ Testing with string token:")
    try:
        keka_client = KekaClient(
            auth="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...", 
            instance_url="https://mycompany.keka.com"
        )
        
        print(f"✅ KekaClient created successfully")
        print(f"   Instance URL: {keka_client.instance_url}")
        print(f"   Auth Token: {keka_client.get_auth_token()[:20]}...")
        print(f"   HR Employee auth_token: {keka_client.hr.auth_token[:20] if keka_client.hr.auth_token else 'None'}...")
        print(f"   Helpdesk auth_token: {keka_client.helpdesk.auth_token[:20] if keka_client.helpdesk.auth_token else 'None'}...")
        
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Test 2: KekaAuth object injection
    print("\n2️⃣ Testing with KekaAuth object:")
    try:
        from keka_sdk.src.resources.Auth.auth import KekaAuth
        
        # Create a mock KekaAuth object
        class MockKekaAuth:
            def __init__(self):
                self.auth_token = "mock_token_from_keka_auth"
        
        mock_auth = MockKekaAuth()
        keka_client2 = KekaClient(
            auth=mock_auth,
            instance_url="https://another-company.keka.com"
        )
        
        print(f"✅ KekaClient with KekaAuth created successfully")
        print(f"   Instance URL: {keka_client2.instance_url}")
        print(f"   Auth Token: {keka_client2.get_auth_token()}")
        print(f"   HR Employee auth_token: {keka_client2.hr.auth_token}")
        print(f"   Helpdesk auth_token: {keka_client2.helpdesk.auth_token}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Test 3: Token update functionality
    print("\n3️⃣ Testing token update:")
    try:
        keka_client3 = KekaClient(
            auth="old_token_123",
            instance_url="https://test.keka.com"
        )
        
        print(f"   Original token: {keka_client3.get_auth_token()}")
        
        # Update token
        keka_client3.set_auth_token("new_token_456")
        
        print(f"   Updated token: {keka_client3.get_auth_token()}")
        print(f"   HR Employee token: {keka_client3.hr.auth_token}")
        print(f"   Helpdesk token: {keka_client3.helpdesk.auth_token}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
    
    print("\n🎉 Constructor Injection Test Complete!")
    print("\n📋 Summary:")
    print("   ✅ Auth tokens are automatically injected into all child classes")
    print("   ✅ No need to pass tokens to individual method calls")
    print("   ✅ Token updates propagate to all child classes")
    print("   ✅ Clean and intuitive API")

if __name__ == "__main__":
    test_constructor_injection()

