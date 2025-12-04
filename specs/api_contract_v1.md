# StellarForge API Contract - MVP Feature Specification

*Goal: To define the single, core endpoint that the MVP SDK will wrap, simplifying the creation of a new astronomical resource. This document serves as the internal specification for developers.*

1. Service Name & Purpose
Service: StellarForge API Purpose: A high-throughput API for managing and classifying newly discovered astronomical objects (stars, planets, comets) in real-time.

2. Core Resource
Resource Name: `Star` Description: A celestial object being registered in the StellarForge catalog.

3. Minimum Viable Product (MVP) Core Method
MVP Method: Create a new Star object. Core Function: Allows clients to submit raw observation data to be processed and catalogued.

4. API Request Specification (The Endpoint)

| Detail | Value | 
| :------------------- | :---------- | 
| HTTP Method | POST | 
| Endpoint Path | /v1/stars | 
| Authentication | Required; must include a valid API key in the X-Api-Key HTTP Header | 

## Required Request Body (JSON)

This is the exact payload the developer must send to the raw API.

| Field | Type | Description |
| :------- | :---- | :---------- | 
| name | str | The provisional designation of the star (for example, `"PROV-2025-ALPHA"`) | 
| coordinates | object | The star's coordinates, contained in a nested object | 
| coordinates.ra | number | Right Ascension (in decimal hours, 0.0 to 24.0); required | 
| coordinates.dec | number | Declination (in decimal degrees, -90.0 to 90.0); required | 
| observed_by | str | The organization or telescope that made the observation; required | 


## Successful Response (HTTP 201 Created)

When successful, the API returns the complete Star object, including system-assigned data.

| Field | Type | Description |
| :------- | :---- | :---------- | 
| star_id | string | The provisional designation of the star (for example, `"PROV-2025-ALPHA"`) | 
| name | string | The provisional designation provided in the request | 
| coordinates | object | The registered coordinates |
| observed_by | string | The observer name |
| registered_at | string | UTC timestamp of registration |
