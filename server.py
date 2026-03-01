#!/usr/bin/env python3
"""
M-Team MCP Server - Convenience entry point when running from repo root.

For pip-installed package, use: mcp-server-mteam  or  python -m mcp_server_mteam
"""

from mcp_server_mteam.server import main

if __name__ == "__main__":
    main()
