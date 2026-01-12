# Awesome MCPs

A collection of MCP (Model Context Protocol) servers for [Claude Code](https://claude.ai/code).

## Available MCPs

| MCP | Description | Status |
|-----|-------------|--------|
| [youtube-music](./youtube-music) | Analyze YouTube Music playlists and get personalized music recommendations | ✅ Ready |

## What is MCP?

MCP (Model Context Protocol) allows Claude Code to connect to external services and tools. Each MCP server provides specific capabilities that extend what Claude can do.

## Installation

Each MCP has its own installation instructions. Click on the MCP name above to see details.

### General Pattern

```bash
# 1. Clone this repository
git clone https://github.com/YOUR_USERNAME/awesome-mcps.git
cd awesome-mcps

# 2. Go to the MCP you want
cd youtube-music

# 3. Install dependencies
pip install -r requirements.txt

# 4. Add to Claude Code
claude mcp add <name> -- python /path/to/server.py
```

## Contributing

Want to add your own MCP?

1. Create a new directory with your MCP name
2. Include:
   - `server.py` - MCP server implementation
   - `requirements.txt` - Python dependencies
   - `README.md` - Installation & usage instructions
   - `skill/SKILL.md` - (Optional) Claude Code skill for better UX
3. Submit a PR!

## License

MIT
