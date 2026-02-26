# M-Team MCP Server

[中文](#中文文档) | [English](#english-documentation)

---

## 中文文档

### 简介

M-Team MCP Server 是一个基于 [FastMCP](https://gofastmcp.com/) 框架开发的 MCP（Model Context Protocol）服务器，让 AI 助手（如 Claude、Cursor 等）能够直接调用 M-Team（馒头）私有种子站的 API，实现资源搜索、种子详情获取和种子文件下载功能。

### 功能列表

| 工具 | 说明 |
|------|------|
| `search_torrents` | 按关键词搜索种子资源，支持多种分类模式 |
| `get_torrent_detail` | 根据种子 ID 获取种子详细信息 |
| `download_torrent` | 根据种子 ID 下载 `.torrent` 文件到本地 |

### 安装

#### 前置要求

- Python 3.10 或以上版本
- M-Team 账号及 API Key

#### 安装步骤

**方式一：从 PyPI 安装（推荐）**

```bash
pip install mteam-mcp
```

**方式二：从源码安装**

1. 克隆或下载本项目：

```bash
git clone https://github.com/07freedom/mteam-mcp.git
cd mteam-mcp
```

2. 安装依赖：

```bash
pip install -r requirements.txt
```

3. 配置 API Key：

复制 `.env_example` 为 `.env`，并填入你的 M-Team API Key：

```bash
cp .env_example .env
```

编辑 `.env` 文件：

```env
MTEAM_API_KEY="your_mteam_api_key_here"
```

> 你可以在 M-Team 网站的个人设置 → API Key 处获取 API Key。

#### 可选环境变量

| 变量名 | 默认值 | 说明 |
|--------|--------|------|
| `MTEAM_API_KEY` | （必填） | M-Team API 鉴权密钥 |
| `MTEAM_API_BASE` | `https://api.m-team.cc/api` | API 根地址 |
| `MTEAM_DOWNLOAD_DIR` | `./seed` | 种子文件保存目录 |

### 在 MCP 客户端中使用

#### Cursor / Claude Desktop 配置

在 MCP 客户端配置文件中添加：

```json
{
  "mcpServers": {
    "mteam": {
      "command": "mteam-mcp",
      "env": {
        "MTEAM_API_KEY": "your_mteam_api_key_here"
      }
    }
  }
}
```

> 若从源码运行，可将 `command` 改为 `python`，`args` 设为 `["/path/to/mteam-mcp/server.py"]`。也可不在配置中填写 `env`，在项目目录创建 `.env` 文件即可。

#### 通过命令行启动（pip 安装后）

```bash
mteam-mcp
```

或

```bash
python -m mteam_mcp
```

#### 从源码运行

```bash
fastmcp run server.py:mcp
# 或
python server.py
```

---

### 工具文档

#### `search_torrents` — 搜索种子

搜索 M-Team 上的种子资源。

**输入参数**

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| `keyword` | string | 是 | — | 搜索关键词，支持中文和英文 |
| `mode` | string | 否 | `"normal"` | 搜索模式，可选值见下表 |
| `page_number` | integer | 否 | `1` | 页码（从 1 开始） |
| `page_size` | integer | 否 | `20` | 每页结果数（最大 100） |

**`mode` 可选值**

| 值 | 说明 |
|----|------|
| `normal` | 普通资源 |
| `adult` | 成人资源 |
| `movie` | 电影 |
| `music` | 音乐 |
| `tvshow` | 剧集 |
| `waterfall` | 瀑布流 |
| `rss` | RSS |
| `rankings` | 排行榜 |
| `all` | 全部 |

**输出示例**

```
Search results for "黑暗骑士" (mode=normal)
Total: 25  |  Page 1, showing 20 items
------------------------------------------------------------
[1125330] The Dark Knight 2008 IMAX UHD BluRay 2160p DDP 5.1 DV HDR x265-hallowed
  Size: 17.74 GB  Seeders: 17  Leechers: 0
  Labels: 中字, 4k, hdr10, DoVi  Discount: PERCENT_50
  IMDB: 9.1  Douban: 9.2
...
```

---

#### `get_torrent_detail` — 获取种子详情

根据种子 ID 获取完整的种子信息。

**输入参数**

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `torrent_id` | string | 是 | 种子 ID，如 `"1125330"` |

**输出示例**

```
Torrent Detail: [1125330]
============================================================
Name       : The Dark Knight 2008 IMAX UHD BluRay 2160p DDP 5.1 DV HDR x265-hallowed
Description: 蝙蝠侠：黑暗骑士崛起|类型: 剧情 / 动作 / 科幻 / 惊悚 / 犯罪
Size       : 17.74 GB  (1 file(s))
Labels     : 中字, 4k, hdr10, DoVi
Discount   : PERCENT_50
Seeders    : 17  Leechers: 0  Completed: 71
Created    : 2026-01-29 15:16:42
Visible    : True  Banned: False
IMDB       : https://www.imdb.com/title/tt0468569/  Rating: 9.1
Douban     : https://movie.douban.com/subject/1851857/  Rating: 9.2
```

---

#### `download_torrent` — 下载种子文件

根据种子 ID 下载 `.torrent` 文件。

**输入参数**

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `torrent_id` | string | 是 | 种子 ID，如 `"1125330"` |

**输出示例**

成功时：
```
Torrent saved to: /home/user/mteam-mcp/seed/[M-TEAM]The.Dark.Knight.2008.IMAX.UHD.BluRay.2160p.DDP.5.1.DV.HDR.x265-hallowed.torrent
```

失败时：
```
Failed to get download token: {'code': '403', 'message': 'Forbidden'}
```

---

### 注意事项

- 本工具仅供个人学习和合法使用，请遵守 M-Team 的使用条款。
- API Key 属于敏感信息，请勿将 `.env` 文件提交到公开代码仓库。
- 下载种子功能需要账号有足够的权限。

---

## English Documentation

### Introduction

M-Team MCP Server is a [FastMCP](https://gofastmcp.com/)-based MCP (Model Context Protocol) server that allows AI assistants (Claude, Cursor, etc.) to interact with the M-Team private torrent tracker API — enabling torrent search, detail retrieval, and `.torrent` file downloads.

### Features

| Tool | Description |
|------|-------------|
| `search_torrents` | Search torrents by keyword with optional category mode |
| `get_torrent_detail` | Get full details for a torrent by its ID |
| `download_torrent` | Download a `.torrent` file to local disk by torrent ID |

### Installation

#### Prerequisites

- Python 3.10 or higher
- An M-Team account with a valid API Key

#### Steps

**Option 1: Install from PyPI (recommended)**

```bash
pip install mteam-mcp
```

**Option 2: Install from source**

1. Clone or download this project:

```bash
git clone https://github.com/07freedom/mteam-mcp.git
cd mteam-mcp
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Configure your API Key:

Copy `.env_example` to `.env` and fill in your M-Team API Key:

```bash
cp .env_example .env
```

Edit `.env`:

```env
MTEAM_API_KEY="your_mteam_api_key_here"
```

> You can obtain your API Key from M-Team's user settings page under API Key.

#### Optional Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `MTEAM_API_KEY` | (required) | M-Team API authentication key |
| `MTEAM_API_BASE` | `https://api.m-team.cc/api` | API base URL |
| `MTEAM_DOWNLOAD_DIR` | `./seed` | Directory to save downloaded torrent files |

### Integration with MCP Clients

#### Cursor / Claude Desktop

Add the following to your MCP client config file:

```json
{
  "mcpServers": {
    "mteam": {
      "command": "mteam-mcp",
      "env": {
        "MTEAM_API_KEY": "your_mteam_api_key_here"
      }
    }
  }
}
```

> For source install, use `"command": "python"` with `"args": ["/path/to/mteam-mcp/server.py"]`. You can also omit `env` and use a `.env` file in the project directory.

#### Command line (after pip install)

```bash
mteam-mcp
```

or

```bash
python -m mteam_mcp
```

#### From source

```bash
fastmcp run server.py:mcp
# or
python server.py
```

---

### Tool Reference

#### `search_torrents` — Search Torrents

Search for torrents on M-Team by keyword.

**Input Parameters**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `keyword` | string | Yes | — | Search keyword (Chinese or English) |
| `mode` | string | No | `"normal"` | Search mode (see table below) |
| `page_number` | integer | No | `1` | Page number (1-based) |
| `page_size` | integer | No | `20` | Results per page (max 100) |

**Available `mode` Values**

| Value | Description |
|-------|-------------|
| `normal` | General resources |
| `adult` | Adult content |
| `movie` | Movies |
| `music` | Music |
| `tvshow` | TV shows |
| `waterfall` | Waterfall view |
| `rss` | RSS |
| `rankings` | Rankings |
| `all` | All categories |

**Example Output**

```
Search results for "The Dark Knight" (mode=movie)
Total: 25  |  Page 1, showing 20 items
------------------------------------------------------------
[1125330] The Dark Knight 2008 IMAX UHD BluRay 2160p DDP 5.1 DV HDR x265-hallowed
  Size: 17.74 GB  Seeders: 17  Leechers: 0
  Labels: 中字, 4k, hdr10, DoVi  Discount: PERCENT_50
  IMDB: 9.1  Douban: 9.2
...
```

---

#### `get_torrent_detail` — Get Torrent Details

Retrieve full information for a specific torrent.

**Input Parameters**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `torrent_id` | string | Yes | Torrent ID, e.g. `"1125330"` |

**Example Output**

```
Torrent Detail: [1125330]
============================================================
Name       : The Dark Knight 2008 IMAX UHD BluRay 2160p DDP 5.1 DV HDR x265-hallowed
Description: 蝙蝠侠：黑暗骑士崛起|类型: 剧情 / 动作 / 科幻 / 惊悚 / 犯罪
Size       : 17.74 GB  (1 file(s))
Labels     : 中字, 4k, hdr10, DoVi
Discount   : PERCENT_50
Seeders    : 17  Leechers: 0  Completed: 71
Created    : 2026-01-29 15:16:42
Visible    : True  Banned: False
IMDB       : https://www.imdb.com/title/tt0468569/  Rating: 9.1
Douban     : https://movie.douban.com/subject/1851857/  Rating: 9.2
```

---

#### `download_torrent` — Download Torrent File

Download a `.torrent` file for the given torrent ID.

**Input Parameters**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `torrent_id` | string | Yes | Torrent ID, e.g. `"1125330"` |

**Example Output**

On success:
```
Torrent saved to: /home/user/mteam-mcp/seed/[M-TEAM]The.Dark.Knight.2008.IMAX.UHD.BluRay.2160p.DDP.5.1.DV.HDR.x265-hallowed.torrent
```

On failure:
```
Failed to get download token: {'code': '403', 'message': 'Forbidden'}
```

---

### License & Disclaimer

- This project is for personal and lawful use only. Please comply with M-Team's Terms of Service.
- Your API Key is sensitive — **never commit your `.env` file to a public repository**.
- Torrent downloads require sufficient account privileges on M-Team.
