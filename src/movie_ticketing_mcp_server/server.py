"""Create a MCP server for movie catalog information."""

import logging

from mcp.server.fastmcp import FastMCP
from mcp.types import CallToolResult, TextContent

from movie_ticketing_mcp_server.http_client import create_client
from movie_ticketing_mcp_server.setting import api_server_settings, mcp_server_settings

logger = logging.getLogger(__name__)


def create_mcp_server():
    mcp = FastMCP(
        "Movie Ticketing MCP Server",
        instructions="This is a server that provides information about movie ticketing.",
        stateless_http=True,
        host=mcp_server_settings.host,
        port=mcp_server_settings.port,
    )

    http_client = create_client(api_server_settings.server_url)

    # Add a simple tool to demonstrate the server
    @mcp.tool(
        name="get_tickets",
        description="Get the tickets information.",
        structured_output=True,
    )
    async def get_tickets(
        owner: str | None = None, catalog_id: str | None = None
    ) -> CallToolResult:
        """Get the ticketing information of a movie."""
        try:
            result = await http_client.get(
                f"{api_server_settings.root_path}/tickets",
                params={"owner": owner, "catalog_id": catalog_id},
            )

            return CallToolResult(
                content=[TextContent(type="text", text=f"{result}")],
                structuredContent=result,
            )
        except Exception as e:
            logger.error(f"Error getting ticketing information : {e}")
            return CallToolResult(
                content=[TextContent(type="text", text=f"Error: {e}")],
            )

    logger.info(f"Initialized {mcp_server_settings.name}...")

    return mcp
