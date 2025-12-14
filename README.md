## Configuration
1. Rename .env.example to .env and change the variables
2. https://fastmcp.mintlify.app/integrations/azure


## Start MCP Server
Start the server with:

`fastmcp run main.py --transport http --port 8000`

## Start the MCP Test client:

`uv run test_client.py`

## Test with MCP inspector

1. `npx @modelcontextprotocol/inspector http://localhost:8000/mcp`

2. Use the Auth Tab to test the flow