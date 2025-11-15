"""Entry point for the movie catalog MCP server."""

import logging
import mcp.server.fastmcp
import fastmcp
from movie_ticketing_mcp_server.fastmcp_server import create_fastmcp_server
from movie_ticketing_mcp_server.server import create_mcp_server
from movie_ticketing_mcp_server.setting import mcp_server_settings

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s.%(msecs)d] [%(levelname)s] [%(name)s] [%(threadName)s:%(thread)d] [%(module)s:%(funcName)s:%(lineno)d] - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[logging.StreamHandler()],
)


def main() -> None:
    server: mcp.server.fastmcp.FastMCP = create_mcp_server()
    server.run(transport="streamable-http")


def fastmcp_main() -> None:
    server: fastmcp.FastMCP = create_fastmcp_server()
    server.run(
        transport="streamable-http",
        host=mcp_server_settings.host,
        port=mcp_server_settings.port,
    )
