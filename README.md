# Awesome MCPs

A collection of MCP servers and hooks for [Claude Code](https://claude.ai/code).

## Repository Structure

```
awesome-mcps/
├── mcp/           # MCP servers
│   └── youtube-music/
└── hooks/         # Claude Code hooks
    └── notification/
```

## MCP Servers

| MCP | Description | Status |
|-----|-------------|--------|
| [youtube-music](./mcp/youtube-music) | Analyze YouTube Music playlists and get personalized music recommendations | Ready |

## Hooks

| Hook | Description | Platform |
|------|-------------|----------|
| [notification](./hooks/notification) | macOS system notification when Claude response completes | macOS |

## What is MCP?

MCP (Model Context Protocol) allows Claude Code to connect to external services and tools. Each MCP server provides specific capabilities that extend what Claude can do.

## What are Hooks?

Hooks are shell commands that execute in response to Claude Code events (e.g., response completion, tool calls). They allow you to customize Claude Code's behavior without modifying the core application.

## Installation

### MCP Servers

Each MCP has its own installation instructions. Click on the MCP name above to see details.

```bash
# 1. Clone this repository
git clone https://github.com/YOUR_USERNAME/awesome-mcps.git
cd awesome-mcps

# 2. Go to the MCP you want
cd mcp/youtube-music

# 3. Install dependencies
pip install -r requirements.txt

# 4. Add to Claude Code
claude mcp add <name> -- python /path/to/server.py
```

### Hooks

Copy the hook configuration to your Claude Code settings:

```bash
# Edit Claude Code settings
vim ~/.claude/settings.json

# Add the hooks section from the hook's settings.json
```

## Contributing

Want to add your own MCP or hook?

### Adding an MCP

1. Create a new directory under `mcp/` with your MCP name
2. Include:
   - `server.py` - MCP server implementation
   - `requirements.txt` - Python dependencies
   - `README.md` - Installation & usage instructions
   - `skill/SKILL.md` - (Optional) Claude Code skill for better UX
3. Submit a PR!

### Adding a Hook

1. Create a new directory under `hooks/` with your hook name
2. Include:
   - `settings.json` - Hook configuration to copy
   - `README.md` - Installation & usage instructions
3. Submit a PR!

## License

MIT
