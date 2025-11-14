# Movie Ticketing MCP Server

An MCP (Model Context Protocol) server that provides movie ticketing information to AI assistants like Claude Code. This server acts as a bridge between AI clients and a backend movie ticketing API.

## Requirements

- **Python 3.12+** (required)
- **uv** (Python package installer)
- Backend API server running at `http://localhost:9000` (or configure via `.env`)

## Quick Start

### 1. Install uv

If you don't have `uv` installed yet:

**macOS/Linux:**
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

**Windows:**
```powershell
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

Or install via pip:
```bash
pip install uv
```

### 2. Install Dependencies

Clone the repository and install dependencies:

```bash
# Navigate to project directory
cd movie-ticketing-mcp-server

# Install dependencies with uv (automatically creates virtual environment)
uv sync
```

This will:
- Create a virtual environment in `.venv/`
- Install all dependencies from `pyproject.toml`
- Install the package in editable mode

### 3. Configure Environment

Copy the example environment file and configure as needed:

```bash
cp .env.example .env
```

Edit `.env` to configure server settings:

```bash
# MCP Server Configuration
MCP_NAME="movie-ticketing-mcp-server"
MCP_HOST="0.0.0.0"
MCP_PORT=9100

# Backend API Server Configuration
API_SERVER_URL="http://localhost:9000"
API_ROOT_PATH="/api/v1"
API_OPENAPI_PATH="/openapi.json"
```

### 4. Run the Server

Start the MCP server:

```bash
# Activate virtual environment first (if not already activated)
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Run the server
uv run movie-ticketing-mcp-server
or 
movie-ticketing-mcp-server
```

The server will start on `http://localhost:9100` and expose the MCP endpoint at `http://localhost:9100/mcp`.


### Adding New Tools

To add a new MCP tool, edit `src/movie_ticketing_mcp_server/server.py`:

```python
@mcp.tool(
    name="your_tool_name",
    description="Description for AI clients",
    structured_output=True,
)
async def your_tool_name(param: str) -> CallToolResult:
    """Tool function docstring."""
    try:
        result = await http_client.get(
            f"{api_server_settings.root_path}/endpoint",
            params={"key": param}
        )

        return CallToolResult(
            content=[TextContent(type="text", text=f"{result}")],
            structuredContent=result,
        )
    except Exception as e:
        logger.error(f"Error: {e}")
        return CallToolResult(
            content=[TextContent(type="text", text=f"Error: {e}")],
        )
```

## Configuration

### MCP Server Settings

Configure via environment variables with `MCP_` prefix:

- `MCP_NAME`: Server name (default: "movie-ticketing-mcp-server")
- `MCP_HOST`: Server host (default: "0.0.0.0")
- `MCP_PORT`: Server port (default: 9100)

### Backend API Settings

Configure via environment variables with `API_` prefix:

- `API_SERVER_URL`: Backend API base URL (default: "http://localhost:9000")
- `API_ROOT_PATH`: API root path (default: "/api/v1")
- `API_OPENAPI_PATH`: OpenAPI spec path (default: "/openapi.json")

## Testing

### Test MCP Server Connection

The server is configured for use with Cursor/Claude Code in `.cursor/mcp.json`:

```json
{
  "mcpServers": {
    "movie-ticketing-mcp-server": {
      "url": "http://localhost:9100/mcp"
    }
  }
}
```
