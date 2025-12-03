# StellarForge SDK Interface Design - Python (Conceptual)

*Goal: Translate the raw HTTP API contract (api_contract_v1.md) into a clean, idiomatic Python interface that prioritizes Developer Experience (DX). This document is the internal blueprint that guides the SDK code implementation.*

1. SDK Client Initialization

The primary component is the `StellarForgeClient`. It manages the connection details and authentication, abstracting these complexities from the developer's application code.

Initialization Signature (Python):

```
class StellarForgeClient:
    """
    Client for interacting with the StellarForge API.
    Handles authentication and request configuration.
    """
    # Requires the API Key, which the SDK will place in the X-Api-Key header (see Step 1).
    def __init__(self, api_key: str): 
        # ... internal setup logic ... 
```

2. MVP Method Signature (The Abstraction)

This method signature takes the nested JSON structure required by the raw API `(coordinates: {ra: ..., dec: ...})` and simplifies it into flat, easy-to-use function arguments.

API Requirement (Raw JSON): `coordinates: {ra: 5.67, dec: -32.11}`
SDK Argument (Simplified Python): `ra: float, dec: float`

SDK Method:
```

    def register_new_star(self, name: str, ra: float, dec: float, observed_by: str) -> Star:
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
        pass
		```


3. The Result Object (Native Data Modeling)

The SDK converts the raw JSON response into a simple, object-oriented `Star` class. This allows the developer to access properties using clean dot notation (for example, `my_star.ra`).

| Property on Star Object | Source Field from API Contract  | Description |
| :------- | :---- | :---------- |
| star.id       | star.id   | Unique system identifier |
| star.name     | name   | Provisional designation |
| star.ra       | coordinates.ra | Right Ascension (flattened from nested object) |
| star.dec      | coordinates.dec | Declination (flattened from nested object) |
| star.observed_by | observed_by | Observer's name |
| star.registered_at | registered_at | UTC registration timestamp |

4. Error Abstraction Mapping

This is the translation layer that maps generic HTTP status codes into specific, idiomatic, and catchable Python exceptions, dramatically improving a developer's ability to handle failures predictably.

| Raw API Response | HTTP Code | Idiomatic SDK Exception Name | Developer-Friendly Action |
| :------- | :---- | :---------- | :---------- |
| Success | 201 Created | Returns Star object | Success |
| Auth Failure | 401 Unauthorized | AuthenticationError | Check initialization of `api_key` |
| Validation Error | 400 Bad Request | InvalidCoordinatesError | Correct the method input parameters (refer to the documentation) |
| Server Error | 500 Internal Error | ServiceUnavailableError | Implement a retry mechanism or alert operations |
