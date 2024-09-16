# Margo Management API Specification

The Margo Management API is used to enable communication between Margo compliant devices and orchestration solutions.

Links below provide further detail regarding the API definition:

  - [Desired State](./workload-api/desired-state-api/desired-state.md)
  - [Deployment Status](./workload-api/device-api/deployment-status.md)
  - [Device Capabilities](./workload-api/device-api/device-capabilities.md)
  - [RootCA Download](./workload-api/onboarding-api/rootca-download.md)


## Management Interface Authorization and Security Details

### Authorization Header
For requests requiring authentication a bearer token MUST be present in the message's `Authorization` header.

You can get the access token by sending a request to the workload orchestration web service's token URL, providing the device's client Id and secret.

```bash
curl -X POST \
-H "Content-Type: application/x-www-form-urlencoded" \
-d "grant_type=client_credentials&client_id=<CLIENT_ID>&client_secret=<CLIENT_SECRET>" \
<WOS_Token_URL>
```
The request's response indicates the access token to use for subsequent requests.

```json
{
  "access_token": "ACCESS_TOKEN",
  "token_type": "Bearer",
  "expires_in": 3600
}
```

Set the `Authorization` headers value to `Bearer <ACCESS_TOKEN>` When making request requiring authorization. For example:

```bash
curl -H "Authorization: Bearer ACCESS_TOKEN" https://wos.example.com/device/2fc3d8e9-8c56-4270-b7d3-8ed30262e5e1
```


### Signing Payloads

The following steps are used to sign a payload

1. Generate a SHA-256 hash value for the request's body
2. Create a digital signature by using the message source certificates's private key to encrypt the the hash value
3. Base-64 encode the certificate's public key and the digital signature in the format of `<public key>;<digital signature>`
3. Include the base-64 encoded string in the request's `X-Payload-Signature` header

### Verifying Signed Payloads

The following steps are used to verify signed payloads

1. Retrieve the public key from the `X-Payload-Signature` header
2. Decrypt the digital signature using the public key to get the original hash value
3. Generate a SHA-256 hash value for the requests's body
4. Ensure the generated hash value matches the hash value from the message

