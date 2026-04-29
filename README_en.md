# gradio_share

> Expose your local port to the internet with a single command — leverages Gradio's free tunnel service, no registration required.

**English** | [中文](README.md)

![CI](https://img.shields.io/github/actions/workflow/status/cicbyte/gradio_share/ci.yml?branch=master&style=flat-square) ![Release](https://img.shields.io/github/v/release/cicbyte/gradio_share?style=flat-square) ![License](https://img.shields.io/github/license/cicbyte/gradio_share?style=flat-square) ![Go Version](https://img.shields.io/github/go-mod/go-version/cicbyte/gradio_share?style=flat-square)

## Features

- **Zero config** — automatically fetches remote frp server, no account needed
- **One command** — get a public URL instantly, e.g. `https://xxx.gradio.live`
- **Cross-platform** — Windows / macOS / Linux, amd64 and arm64
- **72-hour validity** — generated URLs remain active for 72 hours

## Quick Start

### Download from Release

Go to [Releases](https://github.com/cicbyte/gradio_share/releases) to download the package for your platform, then extract and run.

### Build from Source

```bash
git clone https://github.com/cicbyte/gradio_share.git
cd gradio_share
go build -o gradio_share .
```

## Usage

```bash
# Forward localhost:8085 (default)
./gradio_share

# Specify a port
./gradio_share --port 3000

# Use short flags
./gradio_share -p 3000 -a https://api.gradio.app/v2/tunnel-request

# Show help
./gradio_share --help
```

### Flags

| Flag | Short | Type | Default | Description |
|------|-------|------|---------|-------------|
| `--port` | `-p` | int | `8085` | Local port to forward |
| `--address` | `-a` | string | `https://api.gradio.app/v2/tunnel-request` | Gradio share server address |
| `--binPath` | `-b` | string | auto-detect | Path to frpc binary |

### Example Output

```
$ ./gradio_share --port 8081
2024/06/25 17:34:30 frpc path: /usr/local/bin/gradio_share/bin/frpc_linux_amd64
2024/06/25 17:34:30 share server: https://api.gradio.app/v2/tunnel-request
2024/06/25 17:34:30 token: mpJfo24vVB-QGtvXTi1o-2hp5rptbD0i71etVCD_NFU=
2024/06/25 17:34:31 forwarding port:8081
2024/06/25 17:34:32 public URL: https://6cb818bca414994400.gradio.live
2024/06/25 17:34:32 valid for: 72 hours
```

## How It Works

1. Calls the Gradio API to get a remote frp server address
2. Uses the platform-appropriate frpc binary to establish a tunnel
3. Parses the public URL from frpc output
4. Keeps the tunnel running for 72 hours

## Credits

Partially inspired by [gradio-tunneling](https://pypi.org/project/gradio-tunneling/).

## License

[MIT](LICENSE)
