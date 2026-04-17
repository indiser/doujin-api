# 📚 Doujin API

> *Because sometimes you need to programmatically access manga metadata. For research purposes, obviously.*

A blazingly fast™ FastAPI-based REST API that scrapes and serves manga metadata from some hentai website. Built with modern async Python, questionable regex patterns, and just enough web scraping magic to make it work without getting us sued.

## 🎯 Overview

This API provides a clean, RESTful interface to retrieve comprehensive manga information including metadata, tags, recommendations, and image URLs. It leverages CloudFlare bypass techniques (via `curl_cffi`) and BeautifulSoup for parsing, because apparently some hentai website doesn't believe in official APIs. I spent 3 days fighting CloudFlare so you don't have to.

**UPDATE**: The old API got deprecated (RIP). We've rebuilt it from scratch to work with some hentai website's new SvelteKit architecture. Because nothing says "fun weekend" like reverse-engineering someone else's frontend framework.

### Key Features

- ⚡ **Async Everything**: Built on FastAPI with async/await for maximum performance (and to sound impressive in interviews)
- 🔒 **CloudFlare Bypass**: Uses `curl_cffi` to impersonate Chrome and bypass protection (we're basically method actors)
- 📊 **Rich Metadata**: Extracts titles, tags, artists, characters, parodies, and more (everything except your dignity)
- 🖼️ **Image URLs**: Generates direct links to all pages and cover images (no more 404s at 2 AM)
- 🎲 **Recommendations**: Scrapes related content suggestions (the algorithm knows you better than you know yourself)
- 🧹 **Clean JSON**: Returns well-structured, easy-to-consume data (unlike the spaghetti code that generates it)

## 🚀 Getting Started

### Prerequisites

- Python 3.8+ (if you're still on 2.7, we need to have a talk)
- A questionable sense of humor
- No judgment
- Coffee (lots of it)
- The ability to explain this project to your parents without making eye contact

### Installation

1. **Clone the repository** (or just copy-paste like we all do when no one's watching)
   ```bash
   git clone https://github.com/indiser/doujin-api.git
   cd doujin-api
   ```

2. **Install dependencies** (pray your Python environment isn't already broken)
   ```bash
   pip install -r requirements.txt
   ```
   *If this fails, try `pip3`. If that fails, reinstall Python. If that fails, switch to JavaScript. If that fails, become a farmer.*

3. **Run the server** (the moment of truth)
   ```bash
   uvicorn main:app --reload
   ```

   Or with Gunicorn for production (look at you, being all professional):
   ```bash
   gunicorn main:app -k uvicorn.workers.UvicornWorker
   ```

The API will be available at `http://localhost:8000` (assuming nothing caught fire)

## 📖 API Documentation

### Endpoints

#### `GET /`
**Home endpoint** - Returns a friendly reminder that you're supposed to use the actual endpoints.

**Response:**
```json
{
  "Message": "Go To The EndPoint Moron /manga_id=id_number or /docs for swagger fastapi documentation"
}
```
*Note: We actually fixed the "Messege" typo in v2. Character development is real. Also added helpful directions because apparently people need hand-holding.*

---

#### `GET /manga_id={manga_id}`
**Retrieve manga metadata** by ID.

**Parameters:**
- `manga_id` (int): The some hentai website gallery ID

**Example Request:**
```bash
curl http://localhost:8000/manga_id=177013
```
*Pro tip: Don't Google that ID. Trust us. We're trying to protect you.*

**Example Response:**
```json
{
  "id": 177013,
  "title": "Example Title",
  "date": "2023-01-15",
  "media_id": "987654",
  "parodies": ["Original Work"],
  "characters": ["Character Name"],
  "groups": ["Group Name"],
  "categories": ["Manga"],
  "language": ["English"],
  "favorites": 12345,
  "tags": ["tag1", "tag2"],
  "artists": ["Artist Name"],
  "num_pages": 225,
  "media_id": "987654",
  "page_urls": [
    "https://i.some hentai website.net/galleries/987654/1.jpg",
    "https://i.some hentai website.net/galleries/987654/2.jpg"
  ],
  "cover_image": "https://t.some hentai website.net/galleries/987654/cover.jpg",
  "recommendations": [
    {
      "id": 123456,
      "title": "Related Title 1",
      "thumbnail_image": "https://t.some hentai website.net/galleries/123456/thumb.jpg"
    },
    {
      "id": 789012,
      "title": "Related Title 2",
      "thumbnail_image": "https://t.some hentai website.net/galleries/789012/thumb.jpg"
    }
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

- **FastAPI**: Modern, fast web framework for building APIs (finally, a Python framework that doesn't make us want to cry)
- **curl_cffi**: CloudFlare bypass via browser impersonation (we're not hackers, we just play them in production)
- **BeautifulSoup4**: HTML parsing for scraping recommendations and cover images (because regex-ing HTML is a war crime)
- **Uvicorn/Gunicorn**: ASGI server for production deployment (fancy words for "makes the code go brrr")

### How It Works

1. **Request Handling**: FastAPI receives the manga ID via path parameter (the easy part)
2. **Session Management**: Async session with Chrome impersonation bypasses CloudFlare (the "please don't ban us" part)
3. **CDN Configuration**: Fetches dynamic image server URLs from some hentai website's config API (because hardcoding URLs is so 2023)
4. **Data Extraction**: 
   - Regex extracts JSON from SvelteKit's `data-sveltekit-fetched` script tags (yes, we're still parsing JavaScript with regex. Still not proud)
   - Double JSON parsing because SvelteKit wraps everything like a Russian nesting doll
   - BeautifulSoup parses HTML for recommendations and cover images (the civilized approach)
5. **URL Generation**: Uses actual CDN paths from the API with round-robin server selection (we're fancy now)
6. **Defensive Programming**: Strict validation and error handling so the API doesn't explode when some hentai website changes their HTML again (narrator: it will)
7. **Response**: Returns clean, structured JSON with all metadata (the part that makes us look competent)

### Lifespan Management

The API properly manages the async session lifecycle:
- Session created on startup
- Gracefully closed on shutdown
- No resource leaks (we're professionals here, unlike that one project we don't talk about)

## 🔧 Configuration

### Browser Impersonation
The API lets `curl_cffi` handle all the fingerprinting automatically:
```python
session = AsyncSession(impersonate="chrome")
```
*No custom headers needed. We learned our lesson. Let the library do the heavy lifting while we take credit.*

### CDN Server Rotation
Dynamically fetches image servers from some hentai website's config API and uses round-robin distribution:
```python
image_pool = itertools.cycle(image_servers)
```
*Because load balancing is our passion. Also because we read that one blog post about itertools.cycle and wanted to use it.*

### Image Paths
Now uses full paths directly from the API response instead of manually constructing URLs:
- No more guessing file extensions
- No more broken image links at 2 AM
- Actual professional-looking code (we're as shocked as you are)

## 🚦 Future Prospects

Because every good project needs a roadmap of features that may or may not ever get implemented (spoiler: they won't):

### Short-term Goals
- [x] **Rate Limiting**: ~~Add proper rate limiting to avoid getting IP banned (again)~~ DONE! Now limited to 3 requests/second via SlowAPI. Your spam scripts will have to find another victim.
- [ ] **Caching**: Implement Redis caching for frequently requested manga (because hitting the same endpoint 1000 times is apparently a thing)
- [ ] **Error Handling**: More granular error responses (404s, 503s, etc.) instead of just "Error: something broke lol"
- [ ] **Pagination**: Support for browsing multiple manga (for the power users)
- [ ] **Search Endpoint**: Query by tags, artists, or titles (the feature everyone actually wants)
- [ ] **Swagger Docs**: Auto-generated API documentation (FastAPI makes this trivial, so we have no excuse)

### Medium-term Goals
- [ ] **Database Integration**: Store metadata locally for faster access (and to stop hammering their servers)
- [ ] **Proxy Rotation**: Distribute requests across multiple IPs (for when one IP ban isn't enough)
- [ ] **Webhook Support**: Notify when new content from favorite artists drops (we're building a notification system for manga. Let that sink in.)
- [ ] **Batch Requests**: Retrieve multiple manga in a single API call (efficiency is our middle name. Our first name is "Procrastination")
- [ ] **Image Proxy**: Serve images through the API to avoid CORS issues (because CORS is the final boss of web development)
- [ ] **Authentication**: API keys for access control (if you're feeling fancy and want to pretend this is enterprise software)

### Long-term Goals
- [ ] **GraphQL Support**: Because REST is so 2020 (and we want to sound cool at meetups)
- [ ] **WebSocket Streaming**: Real-time updates for new releases (because polling is for peasants)
- [ ] **Machine Learning**: Auto-tagging and content recommendations (throw AI at it until it works)
- [ ] **Mobile SDK**: Native libraries for iOS/Android (so you can use this API on the go, you absolute degenerate)
- [ ] **Blockchain Integration**: Just kidding. We're not that desperate for funding. Yet.
- [ ] **World Domination**: Standard startup goal (currently at 0.00001% completion)

## 🐛 Known Issues

*AKA: Things we know are broken but haven't fixed yet*

- No retry logic for failed requests (if at first you don't succeed, give up immediately)
- Session isn't shared across workers in multi-process deployments (each worker is a lone wolf)
- If some hentai website changes their SvelteKit structure, everything breaks (it's not a bug, it's job security)
- Probably some race conditions we haven't discovered yet (they're like Easter eggs, but worse)
- The API returns "SvelteKit payload not found" when CloudFlare is feeling extra protective (aka Tuesday)

## 🤝 Contributing

Contributions are welcome! Whether it's fixing typos (seriously, please do), adding features, or improving documentation, feel free to submit a PR. We promise to review it within 3-5 business days (or months, who's counting?).

### Development Setup
```bash
# Install dev dependencies
pip install -r requirements.txt

# Run with auto-reload (watch your code break in real-time!)
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

**Contribution Guidelines:**
- Write tests (we don't, but you should)
- Follow PEP 8 (we try, we really do)
- Comment your code (unlike us)
- Don't judge our regex patterns too harshly

## ⚖️ Legal Disclaimer

This project is for educational purposes only. Web scraping may violate the terms of service of the target website. Use responsibly and at your own risk. The authors are not responsible for any misuse of this software.

*Translation: Don't blame us if you get banned. We're just humble developers who built a thing. What you do with it is between you and your ISP.*

## 📝 License

This project is provided as-is with no license specified. Use it, modify it, sell it to venture capitalists for millions (if you do, remember us). We don't care. We're too busy debugging production issues at 3 AM.

## 🙏 Acknowledgments

- **FastAPI**: For making Python web development not painful (finally)
- **curl_cffi**: For solving the CloudFlare problem we didn't want to deal with (you're the real MVP)
- **BeautifulSoup**: Still the GOAT of HTML parsing after all these years (we're not worthy)
- **some hentai website**: For migrating to SvelteKit and breaking our API, forcing us to rebuild everything (thanks for the character development)
- **SvelteKit**: For the nested JSON structure that made us question our life choices
- **Stack Overflow**: For the regex pattern we definitely didn't copy-paste at 2 AM (this time it was 3 AM)
- **Coffee**: The real dependency that should be in requirements.txt
- **Our Therapist**: For listening to us complain about CloudFlare for 3 hours straight

---

<div align="center">

**Built with 💻, questionable life choices, and an unhealthy amount of caffeine**

*If you found this useful, consider starring the repo. Or don't. We're not your mom.*

*Remember: This project exists because someone, somewhere, thought "I could automate this" instead of just using the website like a normal person.*

**⭐ Star this repo if you've ever explained a side project to someone and watched their face slowly transition from interest to concern ⭐**

</div>
