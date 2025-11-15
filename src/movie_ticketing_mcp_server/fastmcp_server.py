"""Create a FastMCP server for movie ticketing information."""

import logging
import httpx

from fastmcp import FastMCP
from movie_ticketing_mcp_server.setting import api_server_settings, mcp_server_settings

logger = logging.getLogger(__name__)


def create_fastmcp_server() -> FastMCP:
    """Create a FastMCP server for movie ticketing information."""

    # Create an HTTP client for your API
    client = httpx.AsyncClient(base_url=api_server_settings.server_url)

    # Load your OpenAPI spec
    openapi_spec = httpx.get(api_server_settings.openapi_url).json()

    # Create the MCP server
    mcp = FastMCP.from_openapi(
        openapi_spec=openapi_spec,
        client=client,
        name="Movie Ticketing MCP Server",
    )

    logger.info(f"Initialized {mcp_server_settings.name}...")

    return mcp
