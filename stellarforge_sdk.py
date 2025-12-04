import time
import random

# --- 1. Custom Exceptions (Error Abstraction Layer) ---
# These map directly to the exceptions defined in the documentation (README.md)

class StellarForgeError(Exception):
    """Base exception for all StellarForge SDK errors."""
    pass

class AuthenticationError(StellarForgeError):
    """Raised when the API key is invalid or missing (HTTP 401)."""
    pass

class InvalidCoordinatesError(StellarForgeError):
    """Raised when the input data fails validation (HTTP 400)."""
    pass

class ServiceUnavailableError(StellarForgeError):
    """Raised for transient server-side issues (HTTP 5xx)."""
    pass

# --- 2. Data Model (The Idiomatic Result Object) ---

class Star:
    """
    Represents a successfully registered star object. 
    This object flattens the nested JSON structure from the raw API response.
    """
    def __init__(self, data: dict):
        # Maps the raw API dictionary keys to clean Python attributes (e.g., star_id -> self.id)
        self.id = data.get('star_id')
        self.name = data.get('name')
        
        # We access the nested 'coordinates' data here to flatten the object for the user
        self.ra = data.get('coordinates', {}).get('ra') 
        self.dec = data.get('coordinates', {}).get('dec')
        
        self.observed_by = data.get('observed_by')
        self.registered_at = data.get('registered_at')

    def __repr__(self):
        # Provides a clean string representation for debugging
        return f"<Star ID={self.id}, Name='{self.name}'>"

# --- 3. Mock API Function (Simulating the Backend) ---

def _mock_api_call(method: str, path: str, headers: dict, body: dict) -> tuple[int, dict]:
    """
    Simulates the HTTP request and response from the StellarForge API.
    Used internally by the client for testing without a real network call.
    It simulates 401, 400, 500, and 201 responses based on specific keys/inputs.
    """
    
    # 1. Authentication Check (Maps to HTTP 401)
    api_key = headers.get('X-Api-Key')
    if not api_key or api_key == "INVALID-KEY-401":
        return 401, {"error": "Authentication Failed", "message": "Invalid API Key provided."}

    # 2. Validation Check (Maps to HTTP 400)
    ra = body.get('coordinates', {}).get('ra')
    # Validation constraint from api_contract_v1.md: RA must be 0-24
    if ra is None or not (0 <= ra <= 24):
        return 400, {"error": "Invalid Input", "message": "Right Ascension (ra) must be between 0 and 24."}

    # 3. Server Error Check (Maps to HTTP 500)
    if api_key == "TRIGGER-500-ERROR":
        return 500, {"error": "Internal Error", "message": "Database write failed. The server is down."}
        
    # 4. Success Case (Maps to HTTP 201 Created)
    star_id = f"SF-{random.randint(1000, 9999)}-{random.randint(1000, 9999)}"
    
    # Construct the response body exactly as specified in api_contract_v1.md
    response_body = {
        "star_id": star_id,
        "name": body["name"],
        "coordinates": body["coordinates"],
        "observed_by": body["observed_by"],
        "registered_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    }
    
    return 201, response_body


# --- 4. Client Implementation (The Abstraction Layer) ---

class StellarForgeClient:
    """The main client for interacting with the StellarForge API."""
    
    def __init__(self, api_key: str):
        self._api_key = api_key
    
    def register_new_star(self, name: str, ra: float, dec: float, observed_by: str) -> Star:
        """
        Registers a new Star object in the StellarForge catalog.
        
        This method implements the clean interface defined in the SDK design document.
        """
        
        # 1. Construct the complex nested API request body (Abstraction in reverse)
        # This translates the flat Python arguments into the nested JSON required by the API.
        request_body = {
            "name": name,
            "coordinates": {
                "ra": ra,
                "dec": dec,
            },
            "observed_by": observed_by,
        }
        
        # 2. Define API Headers (Authentication)
        headers = {
            "X-Api-Key": self._api_key,
            "Content-Type": "application/json"
        }
        
        # 3. Call the Mock API endpoint
        # In a real SDK, this would be an actual network call (e.g., using 'requests' library)
        status_code, response_data = _mock_api_call(
            method="POST",
            path="/v1/stars",
            headers=headers,
            body=request_body
        )
        
        # 4. Error Mapping Logic (Crucial for Developer Experience - DX)
        if status_code == 201:
            # Success: Pass the raw data to the Star model
            return Star(response_data)
        elif status_code == 401:
            # Maps 401 to AuthenticationError
            raise AuthenticationError(response_data.get("message", "Authentication Failed."))
        elif status_code == 400:
            # Maps 400 to InvalidCoordinatesError
            raise InvalidCoordinatesError(response_data.get("message", "Invalid input data."))
        elif status_code >= 500:
            # Maps 5xx to ServiceUnavailableError
            raise ServiceUnavailableError(response_data.get("message", "API Server Error."))
        else:
            # Catch all other unexpected errors
            raise StellarForgeError(f"API returned unexpected status code {status_code}: {response_data}")
