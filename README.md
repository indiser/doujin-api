# 📚 Doujin API

> *Because sometimes you need to programmatically access manga metadata. For research purposes, obviously.*

A blazingly fast FastAPI-based REST API that scrapes and serves manga metadata from nHentai. Built with modern async Python and just enough web scraping magic to make it work.

## 🎯 Overview

This API provides a clean, RESTful interface to retrieve comprehensive manga information including metadata, tags, recommendations, and image URLs. It leverages CloudFlare bypass techniques (via `curl_cffi`) and BeautifulSoup for parsing, because apparently nHentai doesn't believe in official APIs.

### Key Features

- ⚡ **Async Everything**: Built on FastAPI with async/await for maximum performance
- 🔒 **CloudFlare Bypass**: Uses `curl_cffi` to impersonate Chrome and bypass protection
- 📊 **Rich Metadata**: Extracts titles, tags, artists, characters, parodies, and more
- 🖼️ **Image URLs**: Generates direct links to all pages and cover images
- 🎲 **Recommendations**: Scrapes related content suggestions
- 🧹 **Clean JSON**: Returns well-structured, easy-to-consume data

## 🚀 Getting Started

### Prerequisites

- Python 3.8+
- A questionable sense of humor
- No judgment

### Installation

1. **Clone the repository** (or just copy the files, we won't tell)
   ```bash
   git clone https://github.com/indiser/doujin-api.git
   cd fastapi
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the server**
   ```bash
   uvicorn main:app --reload
   ```

   Or with Gunicorn for production:
   ```bash
   gunicorn main:app -k uvicorn.workers.UvicornWorker
   ```

The API will be available at `http://localhost:8000`

## 📖 API Documentation

### Endpoints

#### `GET /`
**Home endpoint** - Returns a friendly reminder that you're supposed to use the actual endpoints.

**Response:**
```json
{
  "Messege": "Go To The EndPoint Moron /manga_id=id_number"
}
```
*Note: Yes, "Messege" is intentionally misspelled. It's a feature, not a bug.*

---

#### `GET /manga_id={manga_id}`
**Retrieve manga metadata** by ID.

**Parameters:**
- `manga_id` (int): The nHentai gallery ID

**Example Request:**
```bash
curl http://localhost:8000/manga_id=177013
```

**Example Response:**
```json
{
  "id": 177013,
  "title": "Example Title",
  "date": "2023-01-15",
  "media_id": "987654",
  "parodies": ["Original Work"],
  "charecters": ["Character Name"],
  "groups": ["Group Name"],
  "categories": ["Manga"],
  "language": ["English"],
  "favorites": 12345,
  "tags": ["tag1", "tag2"],
  "artists": ["Artist Name"],
  "num_pages": 225,
  "page_urls": [
    "https://i.nhentai.net/galleries/987654/1.jpg",
    "https://i.nhentai.net/galleries/987654/2.jpg"
  ],
  "cover_image": "https://t.nhentai.net/galleries/987654/cover.jpg",
  "recommendations": [
    {"id": 123456, "title": "Related Title 1"},
    {"id": 789012, "title": "Related Title 2"}
  ]
}
```

**Error Response:**
```json
{
  "Error": "Error message here"
}
```

## 🏗️ Architecture

### Tech Stack

- **FastAPI**: Modern, fast web framework for building APIs
- **curl_cffi**: CloudFlare bypass via browser impersonation
- **BeautifulSoup4**: HTML parsing for scraping recommendations and cover images
- **Uvicorn/Gunicorn**: ASGI server for production deployment

### How It Works

1. **Request Handling**: FastAPI receives the manga ID via path parameter
2. **Session Management**: Async session with Chrome impersonation bypasses CloudFlare
3. **Data Extraction**: 
   - Regex extracts JSON data from `window._gallery` JavaScript variable
   - BeautifulSoup parses HTML for recommendations and cover images
4. **URL Generation**: Constructs direct image URLs using media ID and page extensions
5. **Response**: Returns clean, structured JSON with all metadata

### Lifespan Management

The API properly manages the async session lifecycle:
- Session created on startup
- Gracefully closed on shutdown
- No resource leaks (we're professionals here)

## 🔧 Configuration

### Headers
The API uses a standard Chrome User-Agent to avoid detection:
```python
"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36..."
```

### Image Extensions
Supports multiple formats with automatic detection:
- `j` → JPG
- `p` → PNG
- `w` → WebP
- `g` → GIF

## 🚦 Future Prospects

Because every good project needs a roadmap of features that may or may not ever get implemented:

### Short-term Goals
- [ ] **Rate Limiting**: Add proper rate limiting to avoid getting IP banned
- [ ] **Caching**: Implement Redis caching for frequently requested manga
- [ ] **Error Handling**: More granular error responses (404s, 503s, etc.)
- [ ] **Pagination**: Support for browsing multiple manga
- [ ] **Search Endpoint**: Query by tags, artists, or titles
- [ ] **Swagger Docs**: Auto-generated API documentation (FastAPI makes this trivial)

### Medium-term Goals
- [ ] **Database Integration**: Store metadata locally for faster access
- [ ] **Proxy Rotation**: Distribute requests across multiple IPs
- [ ] **Webhook Support**: Notify when new content from favorite artists drops
- [ ] **Batch Requests**: Retrieve multiple manga in a single API call
- [ ] **Image Proxy**: Serve images through the API to avoid CORS issues
- [ ] **Authentication**: API keys for access control (if you're feeling fancy)

### Long-term Goals
- [ ] **GraphQL Support**: Because REST is so 2020
- [ ] **WebSocket Streaming**: Real-time updates for new releases
- [ ] **Machine Learning**: Auto-tagging and content recommendations
- [ ] **Mobile SDK**: Native libraries for iOS/Android
- [ ] **Blockchain Integration**: Just kidding. We're not that desperate for funding.
- [ ] **World Domination**: Standard startup goal

## 🐛 Known Issues

- Error handling could be more specific
- No retry logic for failed requests
- Session isn't shared across workers in multi-process deployments

## 🤝 Contributing

Contributions are welcome! Whether it's fixing typos (please do), adding features, or improving documentation, feel free to submit a PR.

### Development Setup
```bash
# Install dev dependencies
pip install -r requirements.txt

# Run with auto-reload
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

## ⚖️ Legal Disclaimer

This project is for educational purposes only. Web scraping may violate the terms of service of the target website. Use responsibly and at your own risk. The authors are not responsible for any misuse of this software.

*Translation: Don't blame us if you get banned.*

## 📝 License

This project is provided as-is with no license specified. Use it, modify it, sell it to venture capitalists for millions. We don't care.

## 🙏 Acknowledgments

- **FastAPI**: For making Python web development not painful
- **curl_cffi**: For solving the CloudFlare problem we didn't want to deal with
- **BeautifulSoup**: Still the GOAT of HTML parsing after all these years
- **nHentai**: For not having an official API and forcing me to build this

---

<div align="center">

**Built with 💻 and questionable life choices**

*If you found this useful, consider starring the repo. Or don't. We're not your mom.*

</div>
