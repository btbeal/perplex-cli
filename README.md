# Perplexity AI Clone

A Perplexity AI clone built with OpenAI Agent SDK and FastAPI, featuring web search capabilities through SerpAPI.

## 🏗️ Architecture

The project is organized into separate modules for maintainability:

- **`backend/main.py`** - FastAPI application and API endpoints
- **`backend/agent.py`** - OpenAI Agent SDK integration and chat logic
- **`backend/tools.py`** - Web search tool using SerpAPI
- **`backend/start.py`** - Startup script with environment validation

## 🚀 Quick Start

### Prerequisites

1. **Python 3.12+** (as specified in pyproject.toml)
2. **OpenAI API Key** - Get one from [OpenAI Platform](https://platform.openai.com/api-keys)
3. **SerpAPI Key** - Get one from [SerpAPI](https://serpapi.com/)

### Installation

1. **Clone and navigate to the backend directory:**
   ```bash
   cd backend
   ```

2. **Install dependencies using Poetry:**
   ```bash
   poetry install
   ```

3. **Set up environment variables:**
   Create a `.env` file in the backend directory:
   ```env
   OPENAI_API_KEY=your_openai_api_key_here
   SERP_API_KEY=your_serpapi_key_here
   ```

4. **Start the application:**
   ```bash
   poetry run python start.py
   ```

   Or run directly:
   ```bash
   poetry run uvicorn main:app --reload
   ```

The API will be available at `http://localhost:8000`

## 📚 API Endpoints

### Chat with AI Assistant
```http
POST /chat
Content-Type: application/json

{
  "message": "What's the latest news about AI?",
  "thread_id": "optional_thread_id_for_conversation_continuity"
}
```

### Direct Web Search
```http
POST /search?query=your+search+query&num_results=5
```

### Health Check
```http
GET /health
```

### Agent Information
```http
GET /agent/info
```

## 🛠️ Development

### Project Structure
```
backend/
├── main.py          # FastAPI application
 ├── agent.py         # OpenAI Agent integration
├── tools.py         # Web search functionality
├── start.py         # Startup script
├── pyproject.toml   # Dependencies and project config
└── .env             # Environment variables (create this)
```

### Adding New Tools

1. **Create tool function in `tools.py`:**
   ```python
   def my_new_tool():
       # Your tool logic here
       pass
   
   def get_my_tool_definition():
       return {
           "type": "function",
           "function": {
               "name": "my_tool",
               "description": "Description of what the tool does",
               "parameters": {
                   # Parameter schema
               }
           }
       }
   ```

2. **Register tool in `agent.py`:**
   ```python
   from tools import get_my_tool_definition, my_new_tool
   
   # Add to tools list in PerplexityAgent.__init__
   self.tools = [
       get_web_search_tool_definition(),
       get_my_tool_definition()
   ]
   
   # Handle in handle_tool_calls method
   elif tool_call.function.name == "my_tool":
       # Handle your tool call
   ```

### API Documentation

Once running, visit `http://localhost:8000/docs` for interactive API documentation powered by FastAPI's automatic OpenAPI integration.

## 🔧 Configuration

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `OPENAI_API_KEY` | Your OpenAI API key | Yes |
| `SERP_API_KEY` | Your SerpAPI key for web search | Yes |

### Model Configuration

The default model is `gpt-4o-mini`. You can change this in `agent.py`:

```python
self.assistant = self.client.beta.assistants.create(
    # ...
    model="gpt-4o",  # or any other supported model
    # ...
)
```

## 🚀 Deployment

For production deployment:

1. **Set `allow_origins` in CORS middleware** (in `main.py`)
2. **Use environment variables for configuration**
3. **Consider using a production ASGI server like Gunicorn**
4. **Implement proper logging and error handling**
5. **Add authentication/authorization as needed**

## 📝 License

This project is open source. Add your preferred license here.