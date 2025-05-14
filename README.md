# Ask the Web

A Streamlit application that answers questions using web search results and provides citations.

## Features

- Web search using DuckDuckGo
- Text extraction from web pages
- AI-powered answers with citations
- Clean and intuitive Streamlit interface
- Docker support for easy deployment

## Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd ask-web
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a .env file:
```bash
cp .env.example .env
```
Edit .env and add your OpenRouter API key.

5. Run the application:
```bash
streamlit run src/main.py
```

## Docker Deployment

Build and run with Docker:
```bash
docker build -t ask-web .
docker run -p 8501:8501 ask-web
```

## Architecture

```
src/
├── main.py              # Streamlit application
├── search/             # Web search module
├── scraper/            # Text extraction module
└── llm/               # LLM integration module
```

## Testing

Run tests with pytest:
```bash
pytest tests/
```

## Dependencies

- streamlit: Web application framework
- beautifulsoup4: HTML parsing
- newspaper3k: Article extraction
- duckduckgo-search: Web search
- openai: LLM integration via OpenRouter

## License

MIT License 