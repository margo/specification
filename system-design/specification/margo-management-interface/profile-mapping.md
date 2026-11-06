# Profile Mapping

> **Note:** This page only documents the intent and is not official part of the specification yet. Once we have identified real-world uses cases where this mapping is required we will define the official mapping schema and language.

Under certain use cases, it may be necessary for the workload fleet manager to understand what a [profile](./profiles.md) characteristic property means. Profile characteristics are defined in such a way as to allow for deployment technology specifications to be added or updated without requiring changes to the workload fleet manager implementation. This means we don't want to require workload fleet manager to have to understand the characteristic schemas in order to use them for matching workloads to workload targets.

## Route and HTTP Methods

```http
PUT    /api/v1/profile/mapping/{targetName}
DELETE /api/v1/profile/mapping/{targetName}
```

- PUT creates or replaces. Mapping updates MUST be atomic.
- DELETE removes the complete mapping for the workload target.

### Route Parameters

|Parameter | Type | Required? | Description|
|----------|------|-----------|------------|
| {workloadTargetId} | string | Y | The unique identifier of the workload target reporting the profile mapping.|

Requests MUST use the following format: `{workloadTargetId}[/{workloadTargetId}]`

- The top-level `workloadTargetId` is required.
- The subsequent `workloadTargetId` is required when reporting mappings for a child workload targets profile.
- `workloadTargetId` MUST include only unreserved characters as specified in [RFC3986](https://www.rfc-editor.org/rfc/rfc3986#section-2.3).

The workload target profile must be registered before reporting the profile mapping.

### Response Codes

| Code | Description |
|------|-------------|
| 200 OK | The mapping document was updated successfully. |
| 201 Created | The mapping document was created successfully. |
| 204 No Content | The mapping document was deleted successfully. |
| 400 Bad Request | PUT: Malformed request body. |
| 403 Forbidden | The request is not authorized by the workload fleet manager's local policy (for example, the client relationship has been retired; see [Authorization](../identity/wfm-identity-profile.md#authorization)). |
| 404 Not Found | PUT: No profile was found for the client for the given `workloadTargetId` or `workloadTargetId/workloadTargetId`<br/> DELETE: No workload target with the given `workloadTargetId` was found for the client. |
| 422 Unprocessable Content | Request body includes a semantic error.  |

## Request Body Attributes

| Field      | Type            | Required?       | Description     |
|------------|-----------------|-----------------|-----------------|
| `{terms}` | TermMap | Y | List of term map entries. |

The mapping is an open object. The workload fleet manager MUST treat it as a dynamic set and MUST NOT assume a particular entry exists. The WFM MAY use a mapping entry only when it knows the corresponding vocabulary and has the necessary information to interpret the resolved value.

> **Note:** Properties will be defined to handled additional information that may be needed such as an indication of unites or data types when the actual uses cases are identified.

## Term Map Attributes

| Field      | Type            | Required?       | Description     |
|------------|-----------------|-----------------|-----------------|
| key | string | Y | The unique characteristic key the term is mapped to to find the value |
| property | string | Y | JSONPath expression as defined by [RFC 9535](https://www.rfc-editor.org/rfc/rfc9535). The JSONPath expression MUST be evaluated relative to the characteristic's `properties` object and MUST resolve to the value used for the mapped vocabulary. |

## Example

> **Note:** This is an example to demonstrate the intent, the `type` and `unit` properties used in the example are not decided on at this point.

Assume Margo agrees a workload fleet manager must be able to determine the vendor, memory and storage totals and CPU cores. The mapping would be defined as follows:

```json
{
	"vendor": {
        "key": "margo.org/nameplate",
        "property": "$.vendor",
		"type": "string"
    },
    "memory": {
		"key": "margo.org/resource/memory",
		"property": "$.total",
		"type": "decimal",
		"unit": "Mi"
	},
	"storage": {
		"key": "margo.org/resource/storage",
		"property": "$.total",
		"type": "decimal",
		"unit": "Gi"
	},
	"cpuCores": {
		"key": "margo.org/resource/cpu",
		"property": "$.cpus[*].cores",
		"type": "integer"
	}
}
```
