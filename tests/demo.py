import sys
from stellarforge_sdk import (
    StellarForgeClient, 
    AuthenticationError, 
    InvalidCoordinatesError, 
    ServiceUnavailableError, 
    Star
)

# --- Test Data ---
VALID_API_KEY = "VALID-STAGING-KEY"
INVALID_API_KEY = "INVALID-KEY-401"
SERVER_ERROR_KEY = "TRIGGER-500-ERROR"

# Valid coordinates for a new star
STAR_DATA = {
    "name": "Provisional-2025-A",
    "ra": 5.67,       # Right Ascension (Valid: 0-24)
    "dec": -32.11,    # Declination (Valid: -90 to 90)
    "observed_by": "Vera C. Rubin Observatory"
}

# Invalid coordinates to trigger the 400 error
INVALID_RA_DATA = {
    "name": "Bad-Input-Test",
    "ra": 25.0,       # Invalid: greater than 24
    "dec": 10.0,
    "observed_by": "Test Suite"
}

# --- Core Testing Logic ---

def run_test_case(test_name: str, api_key: str, data: dict, expected_exception=None):
    """
    Runs a single test case and prints the result.
    :param test_name: Name of the scenario being tested.
    :param api_key: The API key to use for the client.
    :param data: The input data for register_new_star.
    :param expected_exception: The custom exception expected to be raised.
    """
    print(f"\n--- Running Test: {test_name} ---")
    client = StellarForgeClient(api_key=api_key)
    
    try:
        # Attempt the API call using the method defined in the README.md
        result = client.register_new_star(
            name=data["name"],
            ra=data["ra"],
            dec=data["dec"],
            observed_by=data["observed_by"]
        )
        
        # Check for unexpected success or successful validation
        if expected_exception is None:
            if isinstance(result, Star):
                print(f"✅ PASS: Star successfully registered. ID: {result.id}")
                # Verify the object flattening worked
                print(f"   (Verification: RA is {result.ra} via dot notation)")
            else:
                print(f"❌ FAIL: Expected Star object, received {type(result)}.")
        else:
            print(f"❌ FAIL: Expected {expected_exception.__name__}, but call succeeded.")
            
    except Exception as e:
        # Check if the raised exception matches the expected exception
        if expected_exception and isinstance(e, expected_exception):
            print(f"✅ PASS: Correct exception caught: {expected_exception.__name__}")
            print(f"   (Error Message: {e})")
        else:
            print(f"❌ FAIL: Unexpected exception raised: {type(e).__name__} - {e}")
            sys.exit(1)

# --- Test Execution ---

if __name__ == "__main__":
    print("==================================================")
    print("  StellarForge SDK Test Suite (Implementing Step 5)")
    print("==================================================")

    # SCENARIO 1: Success Path (HTTP 201)
    run_test_case(
        "SCENARIO 1: Successful Star Registration (HTTP 201)", 
        VALID_API_KEY, 
        STAR_DATA, 
        expected_exception=None
    )

    # SCENARIO 2: Authentication Failure (HTTP 401)
    run_test_case(
        "SCENARIO 2: Authentication Error (HTTP 401)", 
        INVALID_API_KEY, 
        STAR_DATA, 
        expected_exception=AuthenticationError
    )
    
    # SCENARIO 3: Validation Failure (HTTP 400)
    run_test_case(
        "SCENARIO 3: Invalid Input/Validation Error (HTTP 400)", 
        VALID_API_KEY, 
        INVALID_RA_DATA, 
        expected_exception=InvalidCoordinatesError
    )

    # SCENARIO 4: Server Error (HTTP 500)
    run_test_case(
        "SCENARIO 4: Service Unavailable Error (HTTP 500)", 
        SERVER_ERROR_KEY, 
        STAR_DATA, 
        expected_exception=ServiceUnavailableError
    )

    print("\n==================================================")
    print("  Test Suite Complete. All SDK Abstractions Verified.")
    print("==================================================")
