"""
M-Team MCP Server

Provides MCP tools for interacting with the M-Team (馒头) private torrent tracker:
  - search_torrents    : Search torrents by keyword
  - get_torrent_detail : Get detailed info for a specific torrent
  - download_torrent   : Download a .torrent file by torrent ID

Authentication: MTEAM_API_KEY read from .env file (x-api-key header).
"""

import os
import re

import requests
from dotenv import load_dotenv
from fastmcp import FastMCP

load_dotenv()

API_KEY: str = os.environ.get("MTEAM_API_KEY", "")
BASE_URL: str = os.environ.get("MTEAM_API_BASE", "https://api.m-team.cc/api").rstrip("/")
DOWNLOAD_DIR: str = os.environ.get("MTEAM_DOWNLOAD_DIR", "./seed")

mcp = FastMCP(
    "mteam-mcp",
    instructions=(
        "Tools for searching and downloading torrents from M-Team (馒头). "
        "Requires MTEAM_API_KEY to be set in the .env file."
    ),
)


def _headers() -> dict[str, str]:
    if not API_KEY:
        raise RuntimeError(
            "MTEAM_API_KEY is not set. "
            "Please add it to your .env file (see .env_example)."
        )
    return {
        "Content-Type": "application/json",
        "x-api-key": API_KEY,
    }


def _format_size(size_bytes: int | str | None) -> str:
    """Convert byte count to human-readable string."""
    if size_bytes is None:
        return "unknown"
    try:
        n = int(size_bytes)
    except (ValueError, TypeError):
        return str(size_bytes)
    for unit in ("B", "KB", "MB", "GB", "TB"):
        if n < 1024:
            return f"{n:.2f} {unit}"
        n /= 1024
    return f"{n:.2f} PB"


@mcp.tool
def search_torrents(
    keyword: str,
    mode: str = "normal",
    page_number: int = 1,
    page_size: int = 20,
) -> str:
    """Search torrents on M-Team by keyword.

    Args:
        keyword: Search keyword (supports Chinese / English).
        mode: Search mode. One of: normal, adult, movie, music, tvshow,
              waterfall, rss, rankings, all. Defaults to "normal".
        page_number: Page number (1-based). Defaults to 1.
        page_size: Number of results per page (max 100). Defaults to 20.

    Returns:
        A formatted string listing matching torrents with their IDs, names,
        sizes, seeder/leecher counts, labels, ratings, and discount info.
    """
    url = f"{BASE_URL}/torrent/search"
    body = {
        "keyword": keyword,
        "mode": mode,
        "pageNumber": page_number,
        "pageSize": page_size,
    }
    resp = requests.post(url, json=body, headers=_headers(), timeout=30)
    resp.raise_for_status()
    data = resp.json()

    code = data.get("code")
    message = data.get("message", "")
    payload = data.get("data")

    if str(code) != "0" and message.upper() != "SUCCESS":
        return f"API error {code}: {message}"

    if isinstance(payload, dict):
        items: list = (
            payload.get("list")
            or payload.get("data")
            or payload.get("torrents")
            or []
        )
        total = payload.get("total") or payload.get("totalCount") or len(items)
    elif isinstance(payload, list):
        items = payload
        total = len(payload)
    else:
        return f"Unexpected response format:\n{data}"

    if not items:
        return f'No results found for "{keyword}" (mode={mode}).'

    lines = [
        f'Search results for "{keyword}" (mode={mode})',
        f"Total: {total}  |  Page {page_number}, showing {len(items)} items",
        "-" * 60,
    ]
    for item in items:
        tid = item.get("id", "?")
        name = item.get("name") or item.get("title") or "(no name)"
        size = _format_size(item.get("size"))
        labels = ", ".join(item.get("labelsNew") or []) or "-"
        imdb_rating = item.get("imdbRating") or "-"
        douban_rating = item.get("doubanRating") or "-"
        status = item.get("status") or {}
        seeders = status.get("seeders", "?")
        leechers = status.get("leechers", "?")
        discount = status.get("discount", "-")
        lines.append(
            f"[{tid}] {name}\n"
            f"  Size: {size}  Seeders: {seeders}  Leechers: {leechers}\n"
            f"  Labels: {labels}  Discount: {discount}\n"
            f"  IMDB: {imdb_rating}  Douban: {douban_rating}"
        )

    return "\n".join(lines)


@mcp.tool
def get_torrent_detail(torrent_id: str) -> str:
    """Get detailed information for a specific torrent by its ID.

    Args:
        torrent_id: The numeric torrent ID (e.g. "1125330").

    Returns:
        A formatted string with full torrent details including name, size,
        description, ratings, file count, seeder/leecher counts, etc.
    """
    url = f"{BASE_URL}/torrent/detail"
    # detail endpoint accepts form-encoded data (not JSON)
    detail_headers = {k: v for k, v in _headers().items() if k != "Content-Type"}
    resp = requests.post(url, data={"id": torrent_id}, headers=detail_headers, timeout=30)
    resp.raise_for_status()
    data = resp.json()

    code = data.get("code")
    message = data.get("message", "")
    payload = data.get("data")

    if payload is None:
        return f"API error {code}: {message}"

    item = payload if isinstance(payload, dict) else {}

    tid = item.get("id", torrent_id)
    name = item.get("name") or item.get("title") or "(no name)"
    small_descr = item.get("smallDescr") or "-"
    size = _format_size(item.get("size"))
    numfiles = item.get("numfiles", "?")
    labels = ", ".join(item.get("labelsNew") or []) or "-"
    imdb = item.get("imdb") or "-"
    imdb_rating = item.get("imdbRating") or "-"
    douban = item.get("douban") or "-"
    douban_rating = item.get("doubanRating") or "-"
    created = item.get("createdDate", "-")
    status = item.get("status") or {}
    seeders = status.get("seeders", "?")
    leechers = status.get("leechers", "?")
    times_completed = status.get("timesCompleted", "?")
    discount = status.get("discount", "-")
    visible = status.get("visible", True)
    banned = status.get("banned", False)

    lines = [
        f"Torrent Detail: [{tid}]",
        "=" * 60,
        f"Name       : {name}",
        f"Description: {small_descr}",
        f"Size       : {size}  ({numfiles} file(s))",
        f"Labels     : {labels}",
        f"Discount   : {discount}",
        f"Seeders    : {seeders}  Leechers: {leechers}  Completed: {times_completed}",
        f"Created    : {created}",
        f"Visible    : {visible}  Banned: {banned}",
        f"IMDB       : {imdb}  Rating: {imdb_rating}",
        f"Douban     : {douban}  Rating: {douban_rating}",
    ]
    return "\n".join(lines)


@mcp.tool
def download_torrent(torrent_id: str) -> str:
    """Download a .torrent file for the given torrent ID.

    This tool first obtains a temporary download token from the M-Team API,
    then downloads the .torrent file and saves it to the configured download
    directory (default: ./seed/).

    Args:
        torrent_id: The numeric torrent ID (e.g. "1125330").

    Returns:
        The absolute path to the saved .torrent file on success, or an error
        message on failure.
    """
    token_url = f"{BASE_URL}/torrent/genDlToken"
    token_headers = {
        "accept": "*/*",
        "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
        "x-api-key": API_KEY,
    }
    if not API_KEY:
        raise RuntimeError(
            "MTEAM_API_KEY is not set. "
            "Please add it to your .env file (see .env_example)."
        )

    resp = requests.post(
        token_url, headers=token_headers, data={"id": torrent_id}, timeout=15
    )
    resp.raise_for_status()
    token_data = resp.json()

    if token_data.get("message") != "SUCCESS" or not token_data.get("data"):
        return f"Failed to get download token: {token_data}"

    download_url: str = token_data["data"]

    # Fetch torrent name for a meaningful filename; fall back to ID if unavailable
    torrent_name = torrent_id
    try:
        detail_headers = {k: v for k, v in _headers().items() if k != "Content-Type"}
        detail_resp = requests.post(
            f"{BASE_URL}/torrent/detail",
            data={"id": torrent_id},
            headers=detail_headers,
            timeout=15,
        )
        detail_resp.raise_for_status()
        detail_data = detail_resp.json()
        raw_name = (detail_data.get("data") or {}).get("name") or ""
        if raw_name:
            torrent_name = raw_name
    except Exception:
        pass

    # Replace spaces with dots, then strip illegal filesystem characters
    dotted = torrent_name.replace(" ", ".")
    safe_name = re.sub(r'[<>:"/\\|?*\x00-\x1f]', "", dotted).strip(".")
    if not safe_name:
        safe_name = torrent_id
    filename = f"[M-TEAM]{safe_name}.torrent"
    os.makedirs(DOWNLOAD_DIR, exist_ok=True)
    output_path = os.path.abspath(os.path.join(DOWNLOAD_DIR, filename))

    dl_resp = requests.get(download_url, stream=True, timeout=60)
    dl_resp.raise_for_status()
    with open(output_path, "wb") as f:
        for chunk in dl_resp.iter_content(chunk_size=128 * 1024):
            if chunk:
                f.write(chunk)

    return f"Torrent saved to: {output_path}"


def main() -> None:
    """Entry point for the mteam-mcp console script."""
    mcp.run()


if __name__ == "__main__":
    main()
