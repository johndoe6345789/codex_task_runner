# Codex Backend Endpoints (observed)

The entries below are best-effort documentation based on client fetch traces, Playwright network interception, and the project's polling scripts. Treat these as observational notes; exact field names may vary in the live API.

**Base URL:** `https://chatgpt.com/backend-api`

## Discovered Endpoints Summary

### WHAM (Codex) Endpoints
| Method | Path | Description |
|--------|------|-------------|
| GET | `/wham/tasks/list?limit=N&task_filter=current\|archived\|all` | List tasks |
| GET | `/wham/tasks/{task_id}` | Task detail |
| POST | `/wham/tasks/{task_id}/archive` | Archive a task |
| GET | `/wham/tasks/{task_id}/turns` | List turns for a task |
| GET | `/wham/tasks/{task_id}/turns/{turn_id}/pr` | Get PR status for a turn |
| POST | `/wham/tasks/{task_id}/turns/{turn_id}/pr` | Create PR for a turn |
| POST | `/wham/tasks/{task_id}/turns/{turn_id}/viewed` | Mark turn as viewed |
| GET | `/wham/usage` | Usage stats |
| GET | `/wham/environments` | List environments |
| GET | `/wham/environments/recent` | Recently used environments |
| GET | `/wham/settings/user` | User settings |
| GET | `/wham/github/list-repositories?page=N&per_page=N` | List connected repos |
| GET | `/wham/github/repositories/{repo_id}` | Repository details |

### Account/User Endpoints
| Method | Path | Description |
|--------|------|-------------|
| GET | `/me` | Current user info |
| GET | `/accounts/check/v4-2023-04-27` | Account status |
| GET | `/accounts/mfa_info` | MFA settings |
| GET | `/settings/user` | User settings |
| GET | `/user_granular_consent` | Consent settings |
| GET | `/subscriptions?account_id=...` | Subscription info |

### Connector/Integration Endpoints
| Method | Path | Description |
|--------|------|-------------|
| POST | `/aip/connectors/list_accessible` | List available connectors |
| POST | `/aip/connectors/links/list_accessible` | List connector links |
| GET | `/aip/connectors/oauth_clients?service=github` | OAuth clients |
| GET | `/aip/connectors/{connector_id}/mfa_requirement` | MFA requirements |
| GET | `/connectors/check?connector_names=...` | Check connector status |

### Other Endpoints
| Method | Path | Description |
|--------|------|-------------|
| GET | `/amphora/notifications?limit=N` | Notifications |
| GET | `/celsius/ws/user` | WebSocket user info |
| GET | `/checkout_pricing_config/countries` | Pricing countries |
| GET | `/checkout_pricing_config/configs/{country}` | Country-specific pricing |

---

## API Naming Conventions

The Codex API uses some unconventional naming that reflects its internal architecture:

### "WHAM" (`/backend-api/wham/...`)
The base path for all Codex endpoints. Likely an internal project codename (OpenAI has used whimsical names before - GPT itself started as "Generative Pre-trained Transformer"). WHAM may stand for something like "Workspace Host Agent Manager" or could just be a fun name.

### Task IDs (`task_e_69502ab28bcc8331a29f727e77deb37c`)
- Format: `task_e_<hex_id>`
- The `_e_` likely means "entity" - a common pattern in distributed systems to distinguish entity types
- The hex portion is a unique identifier (possibly UUID-based)

### Turn IDs (`task_e_xxx~assttrn_e_yyy`)
- Format: `<task_id>~<turn_type>trn_e_<hex_id>`
- The tilde `~` acts as a namespace separator, binding turns to their parent task
- `assttrn` = "assistant turn" (Codex's response)
- `usertrn` = "user turn" (the original prompt/request)
- This hierarchical ID allows reconstructing the conversation tree

### Why "Turns"?
The term comes from dialogue theory and conversational AI research. A conversation is modeled as participants "taking turns" speaking - like a game of chess or tennis. Each time the speaker changes, that's a new "turn."

In Codex:
- **User turn**: You submit a task/prompt
- **Assistant turn**: Codex responds with code, commits, PR creation, etc.

This terminology is standard in chatbot/LLM systems (you'll see it in OpenAI's Chat Completions API docs too). It's more precise than "message" because a turn can contain multiple messages, tool calls, or actions - it represents one party's complete contribution before handing control back.

### Turn Mapping Structure
The `turn_mapping` response uses a tree structure with `parent`/`children` fields rather than a flat list. This supports:
- Branching conversations (multiple responses to one prompt)
- Tracking which turn led to which
- The `current_turn_id` points to the active/latest branch

This design mirrors how ChatGPT handles conversation history internally, where you can "regenerate" responses and have multiple branches.

## Authentication
- Many backend calls require an `Authorization: Bearer <token>` header (JWT-like). Replaying cookies and CSRF alone returned `401` during testing.
- Error response example:

```json
{"detail": "Unauthorized"}
```

## Endpoint: Tasks list
- Path: `/backend-api/wham/tasks/list`
- Method: `GET`
- Description: Returns a paginated list of task summaries.

**Query Parameters:**
| Param | Type | Description |
|-------|------|-------------|
| `limit` | int | Max tasks to return (e.g., 19) |
| `task_filter` | string | Filter type: `current`, `archived`, or `all` |

Example requests:
```
GET /backend-api/wham/tasks/list?limit=19&task_filter=current
GET /backend-api/wham/tasks/list?limit=19&task_filter=archived
GET /backend-api/wham/tasks/list?limit=1&task_filter=all
```

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

The PR endpoint supports both GET (check status) and POST (create PR):

**GET - Check PR status:**
```
GET https://chatgpt.com/backend-api/wham/tasks/{task_id}/turns/{turn_id}/pr
```

**POST - Create PR:**
```
POST https://chatgpt.com/backend-api/wham/tasks/{task_id}/turns/{turn_id}/pr
Headers:
- Accept: */*
- Content-Type: application/json
- Authorization: Bearer <JWT_TOKEN>

Body: {}
```

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
GET https://chatgpt.com/backend-api/wham/tasks/{task_id}/turns
Headers:
- Accept: */*
- Authorization: Bearer <JWT_TOKEN>
- oai-client-version, oai-device-id, oai-language, priority, etc.

Credentials: include
```

**Actual response structure** (confirmed via live API):

```json
{
  "turn_mapping": {
    "task_e_xxx~usertrn_e_yyy": {
      "turn": { ... turn details ... },
      "children": [...],
      "parent": null
    },
    "task_e_xxx~assttrn_e_zzz": {
      "turn": { ... turn details ... },
      "children": [],
      "parent": "task_e_xxx~usertrn_e_yyy"
    }
  },
  "current_turn_id": "task_e_xxx~assttrn_e_zzz"
}
```

Key fields:
- `turn_mapping`: Dict mapping turn IDs to turn data with parent/child relationships
- `current_turn_id`: The ID of the latest/current turn (use this for PR creation)

Notes:
- The response does NOT use a simple `turns` or `results` array
- Use `current_turn_id` to get the latest turn for PR creation
- Each turn in `turn_mapping` contains full conversation context including tool calls

Error example when unauthorized:

```json
{"detail": "Unauthorized"}
```

## Endpoint: GitHub Repository Integration

### List Connected Repositories
```
GET /backend-api/wham/github/list-repositories?page=1&per_page=10
```

Returns paginated list of GitHub repositories connected to the user's account.

### Get Repository Details
```
GET /backend-api/wham/github/repositories/{repo_id}
```

Where `repo_id` is the GitHub repository ID (numeric), e.g., `github-1121989012`.

## Endpoint: Environments

### List All Environments
```
GET /backend-api/wham/environments
```

### List Recent Environments
```
GET /backend-api/wham/environments/recent
```

## Endpoint: Usage Stats
```
GET /backend-api/wham/usage
```

Returns usage statistics for the user's Codex account.

## Endpoint: User Settings
```
GET /backend-api/wham/settings/user
```

Returns Codex-specific user settings and preferences.

## Endpoint: Mark Turn as Viewed

Marks a specific turn as viewed by the user (used by the UI to track read status).

```
POST /backend-api/wham/tasks/{task_id}/turns/{turn_id}/viewed
```

Example:
```
POST https://chatgpt.com/backend-api/wham/tasks/task_e_69502ab28bcc8331a29f727e77deb37c/turns/task_e_69502ab28bcc8331a29f727e77deb37c~assttrn_e_69502ab39f108331af3dc29e586011fd/viewed
Headers:
- Authorization: Bearer <JWT_TOKEN>
- Content-Type: application/json

Body: {}
```

This endpoint is called automatically when viewing a task in the Codex UI to update the "unread" status.

## Endpoint: Archive a Task

Archive a task to move it from the "current" list to "archived".

```
POST /backend-api/wham/tasks/{task_id}/archive
Headers:
- Authorization: Bearer <JWT_TOKEN>
- Content-Type: application/json

Body: {}
```

**Response (success):**
```json
{
  "success": true
}
```

This endpoint moves a task from the active/current task list to the archived list. Archived tasks can still be viewed using `task_filter=archived` or `task_filter=all` on the list endpoint.

---

## Task Creation (WebSocket-based)

**Important:** Task creation does NOT use a REST endpoint. It uses WebSocket communication, similar to ChatGPT's conversation streaming.

### WebSocket Connection
```
wss://ws.chatgpt.com/ws/user/{user_id}?verify={timestamp}-{signature}
```

### Initial Handshake
The client sends a connection command with subscription topics:
```json
[
  {"id": 1, "command": {"type": "connect", "presence": {"type": "presence", "state": "foreground"}}},
  {"id": 2, "command": {"type": "subscribe", "topic_id": "conversations"}},
  {"id": 3, "command": {"type": "subscribe", "topic_id": "wham_tasks"}}
]
```

### Server Response
```json
[
  {"id": 1, "type": "reply", "reply": {"type": "connect", "subscriptions": {}}},
  {"id": 2, "type": "reply", "reply": {"type": "subscribe", "topic_id": "conversations", "recovered": false}},
  {"id": 3, "type": "reply", "reply": {"type": "subscribe", "topic_id": "wham_tasks", "recovered": false}}
]
```

### Creating a Task (Sending a Prompt)
Task creation likely follows a pattern similar to ChatGPT messages:
```json
{
  "id": <seq>,
  "command": {
    "type": "wham_create_task",
    "prompt": "Your task description here",
    "environment_id": "<env_id>",
    "repository_id": "<repo_id>"
  }
}
```

**Note:** The exact payload structure needs to be captured by submitting a task in the browser with network inspection enabled. The WebSocket messages are the key to understanding the full protocol.

### Implications for Programmatic Access
To create tasks programmatically, you would need to:
1. Establish a WebSocket connection to `wss://ws.chatgpt.com/ws/user/{user_id}`
2. Authenticate using the verify signature (derived from session token)
3. Subscribe to the `wham_tasks` topic
4. Send the task creation command
5. Listen for task status updates on the WebSocket

This is significantly more complex than REST API calls and requires maintaining a persistent WebSocket connection.