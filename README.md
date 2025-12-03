# StellarForge SDK for Python

*The official Python library for connecting to the StellarForge API. Seamlessly register new astronomical objects and access catalog data.*

## ✨ Features

- Idiomatic Python: Use native Python classes (Star, Coordinates) instead of raw JSON dictionaries
- Built-in Authentication: Simplifies API key handling
- Robust Error Handling: Translates HTTP errors into actionable Python exceptions (for example, AuthenticationError, InvalidCoordinatesError)
- Planned Feature: Automatic retries for transient 5xx errors (Service Unavailable)

## 🚀 Getting Started

1. **Installation**

Install the library using pip:

`bash`

`pip install stellarforge-sdk`

2. Quick Start Example

The quickest way to register a new star in the catalog is shown below. This example demonstrates how to correctly handle potential API errors.
```
import os
from stellarforge import (
    StellarForgeClient,
    AuthenticationError,
    InvalidCoordinatesError,
    ServiceUnavailableError
)

# 1. Initialize the client
# It's recommended to load your API key from an environment variable for security.
API_KEY = os.environ.get("STELLARFORGE_API_KEY")
if not API_KEY:
    raise ValueError("STELLARFORGE_API_KEY environment variable not set.")

client = StellarForgeClient(api_key=API_KEY)

# 2. Define the new celestial object data
star_name = "Provisional-2025-A"
ra_coord = 5.67   # Right Ascension in hours
dec_coord = -32.11 # Declination in degrees
observer = "Vera C. Rubin Observatory"

try:
    # 3. Call the core MVP method
    new_star = client.register_new_star(
        name=star_name,
        ra=ra_coord,
        dec=dec_coord,
        observed_by=observer
    )

    print(f"✅ Success! Star Registered.")
    print(f"ID: {new_star.id}")
    print(f"Name: {new_star.name}")
    print(f"Registered At: {new_star.registered_at}")

# 4. Handle potential errors
except AuthenticationError:
    print("❌ Error: Invalid API Key. Please check your credentials.")

except InvalidCoordinatesError as e:
    print(f"❌ Error: Input Validation Failed. Details: {e}")

except ServiceUnavailableError:
    print("❌ Error: Service temporarily unavailable. Please retry later.")

except Exception as e:
    print(f"❌ An unexpected error occurred: {e}")
    ```

### 🛠 Reference: SDK Classes and Methods

`StellarForgeClient`

| Method | Description |
| :------------------- | :---------- |
| __init__(api_key: str) | Initializes the client with the required authentication key |
| register_new_star(...) -> Star | (MVP) Registers a new star based on observation data |
  
`Star Object`
A native Python object returned upon successful star registration.

| Property | Type  | Description |
| :------- | :---- | :---------- |
| id       | str   | Unique StellarForge identifier |
| name     | str   | Provisional designation |
| ra       | float | Right Ascension (hours) |
| dec      | float | Declination (degrees) |
| registered_at | str | Timestamp of registration |


## SDK Exceptions
These custom exceptions allow developers to write clean, predictable error handling logic.

| Exception | API HTTP Status | Description |
| :------------------- | :---------- | :---------- |
| AuthenticationError | 401 | Raised when the API key is missing or invalid |
| InvalidCoordinatesError | 400 | Raised when input parameters are syntactically or semantically incorrect (for example, coordinates out of range) |
| ServiceUnavailableError | 5xx | Raised for server-side issues |

## ❓ Support

If you encounter issues, please [open an Issue](https://github.com/<repo>/issues) on the GitHub repository.

