# Claude MCP (Multi-Context Processing) Server

A lightweight bridge enabling Claude AI to search the web in real-time. This Flask-based server integrates Claude's advanced capabilities with DuckDuckGo search, allowing the AI to access current information during conversations.

## Project Overview

This project implements a server that enables Claude to perform web searches during conversations. It consists of:

1. **MCP Server**: A Flask server that handles tool calls and performs web searches
2. **Claude Integration**: A client that connects to Claude's API and manages tool use capabilities
3. **Command-line Interface**: A simple way to interact with Claude + web search capabilities

## Features

- 🔍 **Web Search Integration**: Allows Claude to search for information on the web
- 🤖 **Claude 3 API Support**: Works with Claude's latest models and tool use features
- 🌐 **DuckDuckGo Search**: Uses DuckDuckGo for ethical, tracking-free search results
- ⚡ **Fast Responses**: Streamlined architecture for quick information retrieval
- 💬 **Natural Conversation**: Claude can seamlessly incorporate web search results into conversations

## Setup Instructions

### Prerequisites

- Python 3.9 or higher
- Claude API key

### Installation

1. Clone this repository
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Set your Claude API key:
   ```
   # On Windows
   $env:CLAUDE_API_KEY = "your-api-key"
   
   # On Linux/Mac
   export CLAUDE_API_KEY="your-api-key"
   ```

### Running the Server

1. Start the MCP server:
   ```
   python mcp_server.py
   ```
   The server will run on port 5001 by default.

2. Interact with Claude:
   ```
   python ask_claude.py "your question here"
   ```

## Architecture

```
┌─────────────┐     ┌───────────────┐     ┌───────────────┐
│ User Query  │────▶│ Claude Client │────▶│ Claude API    │
└─────────────┘     └───────┬───────┘     └───────┬───────┘
                           │                     │
                           │                     │
                           │                     ▼
                           │             ┌───────────────┐
                           │             │ Tool Call     │
                           │             └───────┬───────┘
                           │                     │
                           ▼                     │
                    ┌───────────────┐            │
                    │ MCP Server    │◀───────────┘
                    └───────┬───────┘
                           │
                           ▼
                    ┌───────────────┐
                    │ Web Search    │
                    └───────────────┘
```

## API Endpoints

- `GET /health`: Health check endpoint
- `GET /`: Server info and available endpoints
- `POST /tool_call`: Process tool calls from Claude

## Usage Examples

Ask Claude about current events:
```
python ask_claude.py "What happened in the world today?"
```

Ask about technical topics:
```
python ask_claude.py "Explain the latest advancements in quantum computing"
```

## License

MIT

## Acknowledgements

- [Anthropic](https://www.anthropic.com/) for Claude AI
- [DuckDuckGo](https://duckduckgo.com/) for search API 