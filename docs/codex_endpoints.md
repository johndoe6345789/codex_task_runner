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

## Observed endpoint: Create PR for a task turn

Example client call (observed via browser fetch trace):

```
POST https://chatgpt.com/backend-api/wham/tasks/task_e_69502ab19e54833183593529fd574f91/turns/task_e_69502ab19e54833183593529fd574f91~assttrn_e_69502ab24a54833189263b19540a6674/pr
Headers:
- Accept: */*
- Content-Type: application/json
- Authorization: Bearer <JWT_TOKEN>
- oai-client-version, oai-device-id, oai-language, priority, etc. (client metadata)

Body: {}
Credentials: include
Referrer: https://chatgpt.com/codex/tasks/task_e_69502ab19e54833183593529fd574f91
```

Notes:
- The request body observed for this endpoint was an empty JSON object (`{}`).
- The request requires `Authorization: Bearer <token>` (JWT-like) for backend access; replaying cookies alone returned `401` during testing.

Best-effort response schema (inferred):

```json
{
  "pr": {
    "number": 17,
    "url": "https://github.com/owner/repo/pull/17",
    "state": "open",
    "created_at": "2025-12-26T13:00:00Z"
  },
  "task_id": "task_e_69502ab19e54833183593529fd574f91",
  "turn_id": "task_e_69502ab19e54833189263b19540a6674~assttrn_e_69502ab24a54833189263b19540a6674",
  "status": "success"
}
```

Error example when unauthorized:

```json
{"detail": "Unauthorized"}
```

Recommendation: to confirm this schema, capture an authenticated response by extracting a valid bearer token from the browser fetch trace or by running a headless browser with the `.env` cookies to let client-side JS obtain the token and then replay the request to record the real response body.

## Observed endpoint: List turns for a task

Example client call (observed via browser fetch trace):

```
GET https://chatgpt.com/backend-api/wham/tasks/task_e_69502ab19e54833183593529fd574f91/turns
Headers:
- Accept: */*
- Authorization: Bearer <JWT_TOKEN>
- oai-client-version, oai-device-id, oai-language, priority, etc. (client metadata)

Referrer: https://chatgpt.com/codex/tasks/task_e_69502ab19e54833183593529fd574f91
Credentials: include
```

Notes:
- The observed request used the `GET` method and no request body (`body` was `null` in the trace).
- The endpoint returns the list of conversational "turns" (assistant/user exchanges) for the given task.
- Requires `Authorization: Bearer <token>`; cookies alone were insufficient during testing.

Best-effort response schema (inferred):

```json
{
  "count": 3,
  "results": [
    {
      "turn_id": "task_e_69502ab19e54833183593529fd574f91~usrtrn_e_69502ab23...",
      "role": "user",
      "text": "Please apply this patch...",
      "created_at": "2025-12-26T12:35:00Z",
      "attachments": []
    },
    {
      "turn_id": "task_e_69502ab19e54833183593529fd574f91~assttrn_e_69502ab24...",
      "role": "assistant",
      "text": "I prepared a patch and opened a PR.",
      "created_at": "2025-12-26T12:40:00Z",
      "diffs": [
        {"path": "src/foo.py", "patch": "@@ -1 +1 @@\n-old\n+new\n"}
      ]
    }
  ],
  "next": null,
  "previous": null
}
```

Error example when unauthorized:

```json
{"detail": "Unauthorized"}
```

Recommendation: capture an authenticated response (via bearer token replay or headless browser) to confirm exact field names and nested structures for `turns`, `diffs`, and any PR-related metadata.