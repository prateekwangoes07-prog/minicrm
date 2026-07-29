# MiniCRM - API Payload Design Guidelines

This document outlines the JSON transfer structure for REST APIs in MiniCRM. For overall coding standards, refer to [MASTER_RULES.md](file:///c:/Users/User/OneDrive/Desktop/MiniCRM/docs/MASTER_RULES.md).

---

## 1. REST Endpoint naming
* Resource endpoints must represent plural nouns: `/api/v1/customers`, not `/api/v1/getCustomer`.
* Sub-resource endpoints denote membership relationships: `/api/v1/leads/{lead_id}/activities`.

---

## 2. Response JSON Standards

### Standard Single Resource
```json
{
  "id": "a8b7c6d5-e4f3-a2b1-c0d9-e8f7a6b5c4d3",
  "name": "Acme Corp",
  "created_at": "2026-07-27T17:15:05Z"
}
```

### Standard Paginated Collection
All list requests support parameter paging (`limit` & `offset`):
```json
{
  "items": [],
  "total": 120,
  "limit": 20,
  "offset": 0
}
```

---

## 3. Error Response Payloads

### Input Schema Validation Error (HTTP 422)
```json
{
  "detail": [
    {
      "loc": ["body", "email"],
      "msg": "invalid email format",
      "type": "value_error"
    }
  ]
}
```

### Server/Process Operational Error (HTTP 400/404/500)
```json
{
  "detail": "Requested lead record was not found.",
  "error_code": "RESOURCE_NOT_FOUND"
}
```
