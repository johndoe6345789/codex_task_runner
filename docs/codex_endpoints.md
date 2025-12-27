# Codex Backend Endpoints (observed)

The entries below are best-effort documentation based on client fetch traces and the project's polling scripts. Treat these as observational notes; exact field names may vary in the live API.

## Authentication
- Many backend calls require an `Authorization: Bearer <token>` header (JWT-like). Replaying cookies and CSRF alone returned `401` during testing.
- Error response example:

```json
{"detail": "Unauthorized"}
```

## Endpoint: Tasks list
- Path (observed): `/backend-api/wham/tasks/list` (query params used for pagination/filtering)
- Method: `GET`
- Description: Returns a paginated list of task summaries.

Example response schema (best-effort):

```json
{
  "count": 123,
  "next": "https://.../tasks/list?page=2",
  "previous": null,
  "results": [
    {
      "id": "task_e_69502ab19e54833183593529fd574f91",
      "title": "Apply patch to repo",
      "status": "open",
      "created_at": "2025-12-26T12:34:56Z",
      "summary": "Short description",
      "repo": "owner/repo",
      "branch": "auto/patch-123"
    }
  ]
}
```

## Endpoint: Task detail
- Path (observed): `/backend-api/wham/tasks/{task_id}`
- Method: `GET`
- Description: Returns full task metadata and related diffs/PR info.

Example response schema:

```json
{
  "id": "task_e_69502ab19e54833183593529fd574f91",
  "title": "Apply patch to repo",
  "description": "Full task description",
  "status": "open",
  "created_at": "2025-12-26T12:34:56Z",
  "updated_at": "2025-12-26T13:00:00Z",
  "repo": "owner/repo",
  "branch": "auto/patch-123",
  "diffs": [
    {
      "path": "src/foo.py",
      "patch": "@@ -1,2 +1,2 @@\n-old\n+new\n"
    }
  ],
  "prs": [
    {
      "number": 17,
      "url": "https://github.com/owner/repo/pull/17",
      "state": "open"
    }
  ]
}
```

## Endpoint: Diff / Raw patch retrieval (observed patterns)
- Path: may be embedded under tasks detail or available at `/backend-api/wham/tasks/{task_id}/diff` or similar.
- Method: `GET`
- Response: raw patch text or JSON containing patch strings (see `diffs` above).

## Endpoint: PR create / update (client-driven)
- Path: not fully observed; client likely calls internal endpoints or the public GitHub API via service layer.
- Example request payload (if present):

```json
{
  "repo": "owner/repo",
  "branch": "auto/patch-123",
  "title": "Apply automated patch",
  "body": "This patch applies...",
  "draft": false
}
```

Example response (success):

```json
{
  "pr_number": 17,
  "url": "https://github.com/owner/repo/pull/17",
  "state": "open"
}
```

## Common error responses

- Unauthorized (401):

```json
{"detail": "Unauthorized"}
```

- Not Found (404):

```json
{"detail": "Not Found"}
```

- Validation errors (400):

```json
{"errors": {"field": ["must be present"]}}
```

---

Notes & next steps:
- These schemas are inferred from observed client requests and common REST patterns; confirm exact schemas by capturing an authenticated request with a valid bearer token or requesting API docs from the service owners.
- If you want, I can try to extract a bearer token from `fetch.txt` and re-run the poll to capture real JSON responses for precise schema extraction.