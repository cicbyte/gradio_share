# gradio_share

> 一条命令，将本地端口暴露到公网 — 复用 Gradio 免费隧道服务，无需注册、无需配置。

[English](README_en.md) | **中文**

![CI](https://img.shields.io/github/actions/workflow/status/cicbyte/gradio_share/ci.yml?branch=master&style=flat-square) ![Release](https://img.shields.io/github/v/release/cicbyte/gradio_share?style=flat-square) ![License](https://img.shields.io/github/license/cicbyte/gradio_share?style=flat-square) ![Go Version](https://img.shields.io/github/go-mod/go-version/cicbyte/gradio_share?style=flat-square)

## 功能特性

- **零配置** — 自动获取远程 frp 服务器，无需注册账号
- **一条命令** — 启动即可获得公网 URL，如 `https://xxx.gradio.live`
- **多平台** — 支持 Windows / macOS / Linux，amd64 和 arm64
- **72 小时有效** — 生成的公网 URL 可持续使用 72 小时

## 快速开始

### 从 Release 下载

前往 [Releases](https://github.com/cicbyte/gradio_share/releases) 下载对应平台的压缩包，解压后直接运行。

### 从源码构建

```bash
git clone https://github.com/cicbyte/gradio_share.git
cd gradio_share
go build -o gradio_share .
```

## 使用方法

```bash
# 默认转发 localhost:8085
./gradio_share

# 指定端口
./gradio_share --port 3000

# 使用短参数
./gradio_share -p 3000 -a https://api.gradio.app/v2/tunnel-request

# 查看帮助
./gradio_share --help
```

### 参数说明

| 参数 | 短参数 | 类型 | 默认值 | 说明 |
|------|--------|------|--------|------|
| `--port` | `-p` | int | `8085` | 要转发的本地端口 |
| `--address` | `-a` | string | `https://api.gradio.app/v2/tunnel-request` | Gradio 分享服务器地址 |
| `--binPath` | `-b` | string | 自动检测 | frpc 二进制文件路径 |

### 输出示例

```
$ ./gradio_share --port 8081
2024/06/25 17:34:30 frpc程序路径: /usr/local/bin/gradio_share/bin/frpc_linux_amd64
2024/06/25 17:34:30 分享服务器地址: https://api.gradio.app/v2/tunnel-request
2024/06/25 17:34:30 安全令牌: mpJfo24vVB-QGtvXTi1o-2hp5rptbD0i71etVCD_NFU=
2024/06/25 17:34:31 转发的端口:8081
2024/06/25 17:34:32 访问地址：https://6cb818bca414994400.gradio.live
2024/06/25 17:34:32 连接有效期:72小时
```

## 工作原理

1. 调用 Gradio API 获取远程 frp 服务器地址
2. 使用对应平台的 frpc 二进制建立隧道
3. 从 frpc 输出中解析公网 URL
4. 保持隧道运行 72 小时

## 参考

部分逻辑参考 [gradio-tunneling](https://pypi.org/project/gradio-tunneling/) 实现。

## 许可证

[MIT](LICENSE)
