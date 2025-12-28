# MCP Session Log and Current Application State

This page records the interactive work performed with the MediaWiki MCP server, the test steps run, and the current application state as of 2025-12-28.

Conversation summary (high level)
- Goal: Install and run the MediaWiki MCP server against a local MediaWiki at `http://localhost:8080`, run it in Docker attached to the existing MediaWiki stack, verify connectivity, and wire it into the workspace/VS Code.
- Actions performed: cloned upstream repo, created `config.json`, built Docker image `mediawiki-mcp-server:local`, started container `mediawiki-mcp` attached to `mediawiki_default`, resolved a port conflict on host port `3000`, verified MCP health and in-network MediaWiki API access, created workspace glue files, registered the MCP in VS Code, and published documentation to the wiki.

Files added to repository
- `MediaWiki-MCP-Server/config.json` — runtime config pointing at `http://mediawiki:8080` for in-network access.
- `docker-compose.mcp.yml` — helper compose to build/run the MCP attached to `mediawiki_default`.
- `mcp.client.json` and `.vscode/settings.json` — VS Code/IDE integration entries for the MCP server.
- `docs/MCP_INTEGRATION.md` — integration summary (published to wiki as `MCP Integration`).
- `scripts/publish_to_wiki.py` — helper Python script that publishes a docs file to the local MediaWiki via the REST/API login+edit flow.
- `scripts/codex_cli.py` — updated to include a `publish-mcp` command that calls the publish script.

What was verified
- MCP health endpoint: `http://localhost:3000/health` → 200 OK, body `{"status":"ok"}`.
- In-network API access: an ephemeral container attached to `mediawiki_default` successfully queried `http://mediawiki/api.php?action=query&meta=siteinfo&format=json` and received site info (site name "Bot Wiki", MediaWiki 1.45.1).
- The integration summary (`docs/MCP_INTEGRATION.md`) was published to the wiki (page title: `MCP Integration`).

Publish performed
- Script used: `scripts/publish_to_wiki.py`
- Credentials used: bot account (username provided by the user). Credentials are NOT stored in repository files.
- Result: Page created — title: `MCP Integration` (pageid 3, revision 4). See `docs/MCP_PUBLISH_RESULT.md` for details.

Current application state
- Docker: container `mediawiki-mcp` running from image `mediawiki-mcp-server:local` attached to `mediawiki_default`, host port `3000` published to container `3000`.
- Wiki: local MediaWiki accessible at `http://localhost:8080`; the published pages:
  - `MCP Integration`: [http://localhost:8080/index.php/MCP_Integration](http://localhost:8080/index.php/MCP_Integration)
  - Session log (this page) will be published as `MCP Integration — Session Log`.
- Workspace: `publish-mcp` CLI stub added to `scripts/codex_cli.py` to call the publish helper.

How to re-run publish locally

```bash
# from workspace root
PYTHONPATH="$PWD/src" venv/bin/python scripts/codex_cli.py publish-mcp <BOT_USERNAME> <BOT_PASSWORD> --title "MCP Integration — Session Log"
```

Notes and next steps
- If you want MCP-based publishing (i.e., call the `create-page` tool via the MCP transport), I can implement a Node client using the `@modelcontextprotocol/sdk` and call the `create-page` tool. That will require installing npm dependencies and having the MCP HTTP transport session available.
- If you'd like me to merge the MCP service into your existing MediaWiki compose stack, I can open a PR patch to the compose file.

Sensitive data
- The bot credentials used for the publish were only used in-memory for the API call and were not written to files. If you want credentials recorded, add them to `MediaWiki-MCP-Server/config.json` (not recommended in plaintext in repo).

Generated: 2025-12-28
