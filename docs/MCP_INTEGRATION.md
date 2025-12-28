# MediaWiki MCP Integration — Summary

This document records the work performed to install and test the MediaWiki MCP server against a local MediaWiki instance.

Summary
- Target wiki: http://localhost:8080 (running in Docker compose)
- MCP server: built from the upstream `MediaWiki-MCP-Server` repository and run in Docker as `mediawiki-mcp` attached to the `mediawiki_default` network
- Transport: MCP Streamable HTTP (MCP_TRANSPORT=http) on host port 3000

What was done
- Cloned the upstream repo and created `MediaWiki-MCP-Server/config.json` configured to use the in-network address `http://mediawiki:8080`.
- Built a local Docker image `mediawiki-mcp-server:local` from the repository `Dockerfile` and started a detached container `mediawiki-mcp` on the `mediawiki_default` network.
- Resolved a host `:3000` port conflict (stopped the prior local process) and restarted the container successfully.
- Verified MCP health: `http://localhost:3000/health` → `{"status":"ok"}`.
- Verified in-network connectivity: an ephemeral container on `mediawiki_default` queried `http://mediawiki:8080/api.php?action=query&meta=siteinfo&format=json` and the MediaWiki API returned site info (site name "Bot Wiki", MediaWiki 1.45.1).

Files added to workspace
- `MediaWiki-MCP-Server/config.json` — MCP runtime config pointing to `http://mediawiki:8080`.
- `docker-compose.mcp.yml` — workspace compose wrapper for building/running the MCP attached to `mediawiki_default`.
- `mcp.client.json` — client entries for starting the MCP via Docker or using direct HTTP.
- `.vscode/settings.json` — MCP entries registered with VS Code. The MCP was also added via the VS Code CLI.

Notes on authentication
- No credentials (bot password or token) were configured in `config.json`. Authenticated operations (page edits/uploads) require a MediaWiki account token or bot password. Provide credentials if you want the MCP to perform edits.

Publishing this summary to the wiki
If you want this summary published as a wiki page, you can either:

1) Use the MediaWiki API directly (example `curl`):

```bash
# 1) Get login token
curl -s "http://localhost:8080/api.php?action=query&meta=tokens&type=login&format=json" \
  | jq -r .query.tokens.logintoken

# 2) Log in (replace USER and PASS)
curl -s -c cookies.txt -d "action=login&lgname=USER&lgpassword=PASS&lgtoken=TOKEN&format=json" \
  "http://localhost:8080/api.php"

# 3) Get CSRF token
curl -s -b cookies.txt "http://localhost:8080/api.php?action=query&meta=tokens&format=json" \
  | jq -r .query.tokens.csrftoken

# 4) Create or edit page (replace PAGE_TITLE and the token)
curl -s -b cookies.txt -d "action=edit&title=PAGE_TITLE&text=$(< docs/MCP_INTEGRATION.md)&token=CSRF_TOKEN&format=json" \
  "http://localhost:8080/api.php"
```

2) Use the MCP server tooling (preferred if you have an MCP client configured). This requires credentials configured in `MediaWiki-MCP-Server/config.json` (fields: `token`, `username`, `password`). If you provide credentials and want me to publish via MCP, I can attempt the publish step.

Next steps you may want
- Provide a bot account token or bot password in `MediaWiki-MCP-Server/config.json` if you want the MCP to create/update pages.
- I can attempt an automated publish to the wiki (via MCP or the MediaWiki API) once credentials are supplied.

If you want me to publish this now, reply with how you'd like to authenticate (MediaWiki bot password, username+password, or a pre-generated edit token with instructions), and I will attempt the publish and report the result.

---
Generated on 2025-12-28.
