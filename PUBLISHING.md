# 发布到 PyPI

## 前置准备

1. 注册 [PyPI](https://pypi.org/account/register/) 账号
2. 安装构建工具：

```bash
pip install build twine
```

## 构建

```bash
python -m build
```

产物将生成在 `dist/` 目录：
- `mteam_mcp-0.1.0-py3-none-any.whl` - wheel 包
- `mteam_mcp-0.1.0.tar.gz` - 源码包

## 发布

### 首次发布（需注册 PyPI 账号）

```bash
twine upload dist/*
```

按提示输入 PyPI 用户名和密码。

### 使用 API Token（推荐）

1. 在 PyPI 创建 [API Token](https://pypi.org/manage/account/token/)
2. 创建 `~/.pypirc`：

```ini
[pypi]
username = __token__
password = pypi-xxxxxxxxxxxxxxxxxxxxxxxx
```

3. 上传：

```bash
twine upload dist/*
```

## 版本更新

发布新版本前，在 `pyproject.toml` 中修改 `version` 字段，例如：

```toml
version = "0.1.1"
```

然后重新构建并上传。
