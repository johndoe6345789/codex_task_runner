Running MediaWiki MCP Server in Docker
-------------------------------------

Quick start (build and run):

```bash
cd MediaWiki-MCP-Server
docker compose up -d --build
```

This will build the image from the repository `Dockerfile`, mount
`config.json` into the container at `/etc/mcp/config.json`, and expose
the MCP HTTP transport on `localhost:3000`.

Network considerations
- If your MediaWiki is running on the Docker host at `localhost:8080`,
  the provided `config.json` uses `http://host.docker.internal:8080` so
  the container can reach the host service.
- If MediaWiki runs in Docker Compose in the same Docker network, edit
  `config.json` and set the wiki `server` to use the MediaWiki service
  name (for example `http://mediawiki:8080`), then add an external
  network block to `docker-compose.yml` matching the MediaWiki stack's
  network name so both services can communicate.

Stopping and removing:

```bash
docker compose down
```

Logs:

```bash
docker compose logs -f
```

If you want, I can attach the MCP container to your existing MediaWiki
Compose network automatically — tell me the MediaWiki compose project
directory or the Docker network name. 
