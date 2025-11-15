"""Create a FastMCP server for movie ticketing information."""

import logging
from fastmcp.server.openapi import MCPType, RouteMap
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
        mcp_names={
            "issue_tickets_tickets_issue_post": "issue_ticket",
            "refund_tickets_tickets_refund_post": "refund_ticket",
            "get_ticket_tickets__ticket_id__get": "get_ticket_by_id",
            "get_ticket_list_tickets_get": "get_tickets",
        },
        route_maps=[
            RouteMap(
                tags={"health"},
                mcp_type=MCPType.EXCLUDE,
            ),
        ],
    )

    logger.info(f"Initialized {mcp_server_settings.name}...")

    return mcp
