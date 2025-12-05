# Technical Documentation Portfolio: StellarForge Python SDK

## 🌟 Project Overview

This project simulates the complete documentation and development workflow for a new Python SDK, **StellarForge**, designed to interact with an astronomical object registration API. The goal was to demonstrate a fundamental understanding of **SDK abstraction, developer experience (DX), and the technical documentation life cycle**.

The SDK transforms a complex, low-level HTTP API into an intuitive, idiomatic Python library, making it easy for developers to submit new celestial observations.

## 5-Step Documentation Workflow

The project followed a five-step documentation-driven development process:

| Step | Artifact Produced | Purpose & Audience | Concept Demonstrated |
| :------- | :---- | :---------- | :---------- | 
| 1. API Contract | `api_contract_v1.md` | Internal: Defined the mandatory behavior of the back-end API (JSON payload, HTTP status codes, data constraints) | API Specification | 
| 2. Interface Blueprint | `sdk_interface_design_blueprint.md` | Internal/Technical Writer: Designed the high-level class structure, method signatures, and determined how to abstract complexity (Flattening Objects, Error Mapping) | Abstraction & DX Design | 
| 3. Public Documentation | `README.md` | Public: The developer's quick-start guide and method reference | Public Documentation | 
| 4. Core Implementation | `stellarforge_sdk.py` | Product Code: Wrote the Python logic to implement the abstraction from Step 2 | Idiomatic Code Design | 
| 5. Quality Assurance | demo.py | QA/Demo: A test script to prove the implementation matches the documentation across all scenarios (Success, 401, 400, 500) | Reliability & Testing | 

## Core Concept Demonstrated: Abstraction & Error Mapping
The primary technical challenge solved was transforming the low-level API response into a superior developer experience (DX).

### DX Comparison: Raw API vs. SDK

| Low-Level API (Bad DX) | High-Level SDK (Good DX) |
| ----------------------- | ------------------------ |
| **Data:** Nested JSON object (e.g., `response['data']['coordinates']['ra']`) | **Abstraction:** Flattened Python object (`Star.ra`) |
| **Errors:** Generic HTTP status codes (e.g., `401 Unauthorized`) | **Abstraction:** Custom Python exceptions (`AuthenticationError`) |


## 💾 Final Artifacts

1. Public Documentation (`README.md`)

This is the primary user guide, focusing on a quick start and error handling. 

``` 
StellarForge SDK for Python

<p align="center">
  <em>The official Python library for connecting to the StellarForge API. Seamlessly register new astronomical objects and access catalog data.</em>
</p>

## ✨ Features

- **Idiomatic Python:** Use native Python classes (like `Star`) instead of raw JSON dictionaries.
- **Built-in Authentication:** Simplifies API key handling by automatically managing the `X-Api-Key` header.
- **Robust Error Handling:** Translates HTTP errors (401, 400, 5xx) into actionable Python exceptions (e.g., `AuthenticationError`).

## 🚀 Getting Started

### 2. Quick Start Example: Register a New Star

```python
import os
from stellarforge import (
    StellarForgeClient,
    AuthenticationError,
    InvalidCoordinatesError,
    ServiceUnavailableError
)

# ... initialization and data setup ...

try:
    # 3. Call the core MVP method
    new_star = client.register_new_star(
        name=star_name,
        ra=ra_coord,
        dec=dec_coord,
        observed_by=observer
    )

    print(f"✅ Success! Star Registered. ID: {new_star.id}")

# 4. Handle potential errors using custom exceptions
except AuthenticationError:
    print("❌ Error: Invalid API Key. Please check your credentials.")

except InvalidCoordinatesError as e:
    print(f"❌ Error: Input Validation Failed. Details: {e}")
# ...

4. Presentation Script Equivalent: Demonstrating the Concepts

While Steps 1, 2, and 3 result in non-executable documents, the enforcement of their rules is visible in the code. This is how you demonstrate the concepts to an employer:

### Demonstrating Step 1: The API Contract

The contract defined the mandatory server behavior, including required validation (`RA` between 0 and 24) and error codes. We can show this is enforced in the `stellarforge_sdk.py` mock function:

```
from typing import Tuple, Dict, Any

class StellarForgeClient:
    """
    Client for interacting with the StellarForge API.
    Handles authentication and request configuration.
    """

    def __init__(self, api_key: str):
        # Store the API key for use in requests
        self.api_key = api_key

    def register_new_star(self, name: str, ra: float, dec: float, observed_by: str) -> "Star":
        """
        Registers a new Star object in the StellarForge catalog.

        :param name: The provisional designation. (String)
        :param ra: Right Ascension (decimal hours, 0.0 to 24.0). (Float)
        :param dec: Declination (decimal degrees, -90.0 to 90.0). (Float)
        :param observed_by: The observer or telescope name. (String)
        :returns: A fully populated Star object upon successful HTTP 201.
        :raises AuthenticationError: If the API key is invalid (HTTP 401).
        :raises InvalidCoordinatesError: If input data fails validation (HTTP 400).
        :raises ServiceUnavailableError: If the API server fails (HTTP 5xx).
        """
        headers = {"X-Api-Key": self.api_key}
        body = {
            "name": name,
            "coordinates": {"ra": ra, "dec": dec},
            "observed_by": observed_by
        }

        status, response = _mock_api_call("POST", "/stars", headers, body)

        if status == 201:
            return Star(**response)
        elif status == 401:
            raise AuthenticationError(response.get("message", "Invalid API Key"))
        elif status == 400:
            raise InvalidCoordinatesError(response.get("message", "Invalid coordinates"))
        elif status >= 500:
            raise ServiceUnavailableError("Service temporarily unavailable")
        else:
            raise Exception(f"Unexpected error: {response}")

# Mock API call (from your earlier snippet)
def _mock_api_call(method: str, path: str, headers: dict, body: dict) -> Tuple[int, Dict[str, Any]]:
    """Simulates the HTTP behavior defined in the API Contract."""

    ra = body.get('coordinates', {}).get('ra')
    if ra is None or not (0 <= ra <= 24):
        return 400, {"error": "Invalid Input", "message": "Right Ascension (ra) must be between 0 and 24."}

    api_key = headers.get('X-Api-Key')
    if not api_key or api_key == "INVALID-KEY-401":
        return 401, {"error": "Authentication Failed", "message": "API key missing or invalid."}

    return 201, {
        "id": "mock-star-123",
        "name": body["name"],
        "ra": body["coordinates"]["ra"],
        "dec": body["coordinates"]["dec"],
        "observed_by": body["observed_by"],
        "registered_at": "2025-12-04T16:44:00Z"
    }

# Example Star class
class Star:
    def __init__(self, id: str, name: str, ra: float, dec: float, observed_by: str, registered_at: str):
        self.id = id
        self.name = name
        self.ra = ra
        self.dec = dec
        self.observed_by = observed_by
        self.registered_at = registered_at

# Example custom exceptions
class AuthenticationError(Exception): pass
class InvalidCoordinatesError(Exception): pass
class ServiceUnavailableError(Exception): pass
``` 

Presenter Narrative: "For Step 1, I created the API Contract document. Its importance is demonstrated here: the `_mock_api_call` function is a literal, executable representation of that contract's rules. It proves that the validation constraints and error codes defined in the specification are the foundation for all subsequent code."
