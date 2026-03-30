from fastapi import FastAPI
import re
from bs4 import BeautifulSoup
from datetime import datetime
import json
from curl_cffi.requests import AsyncSession
from contextlib import asynccontextmanager
import itertools

session = AsyncSession(impersonate="chrome")

@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    await session.close()

app=FastAPI(lifespan=lifespan)

async def getManga(id: int):
    nhentai_url = f"https://nhentai.net/g/{id}/"
    config_api_url = "https://nhentai.net/api/v2/config"
    
    try:
        # 1. NO CUSTOM HEADERS. Let curl_cffi handle the fingerprinting automatically.
        response = await session.get(url=nhentai_url)
        
        # 2. PROPER ASYNC AWAIT for the configuration API
        config_response = await session.get(url=config_api_url)
        
        if response.status_code != 200:
            return {"Error": f"Failed to fetch page. Status: {response.status_code}"}

        # Handle CDN Configuration safely
        image_servers = ["https://i.nhentai.net"]
        thumb_servers = ["https://t.nhentai.net"]
        if config_response.status_code == 200:
            config_data = config_response.json()
            image_servers = config_data.get("image_servers", image_servers)
            thumb_servers = config_data.get("thumb_servers", thumb_servers)

        image_pool = itertools.cycle(image_servers)
        
        data_payload = {}
        json_pattern = r'<script type="application/json" data-sveltekit-fetched data-url="/api/v2/galleries/.*?">(.*?)</script>'
        match = re.search(json_pattern, response.text, re.DOTALL)
        
        # 3. STRICT VALIDATION. Do not proceed if the core payload is missing.
        if not match:
            return {"Error": "SvelteKit payload not found. WAF block or site structure changed."}

        raw_script_content = match.group(1)
        svelte_wrapper = json.loads(raw_script_content)
        gallery_data = json.loads(svelte_wrapper.get('body', '{}'))

        media_id = gallery_data.get('media_id')
        pages = gallery_data.get('pages', [])
        page_urls = []

        for page in pages:
            path = page.get('path')
            if path:
                current_server = next(image_pool)
                page_urls.append(f"{current_server}/{path}")

        # 4. DEFENSIVE EXTRACTION. Prevent KeyErrors from crashing the server.
        tags = gallery_data.get('tags', [])
        data_payload = {
            'id': gallery_data.get('id'),
            'title': gallery_data.get('title', {}).get('english'),
            'date': datetime.fromtimestamp(gallery_data.get('upload_date', 0)).strftime('%Y-%m-%d') if gallery_data.get('upload_date') else None,
            'parodies': [tag.get('name') for tag in tags if tag.get('type') == 'parody'],
            'characters': [tag.get('name') for tag in tags if tag.get('type') == 'character'],
            'groups': [tag.get('name') for tag in tags if tag.get('type') == 'group'],
            'categories': [tag.get('name') for tag in tags if tag.get('type') == 'category'],
            'language': [tag.get('name') for tag in tags if tag.get('type') == 'language'],
            'favorites': gallery_data.get('num_favorites', 0),
            'tags': [tag.get('name') for tag in tags if tag.get('type') == 'tag'],
            'artists': [tag.get('name') for tag in tags if tag.get('type') == 'artist'],
            'num_pages': gallery_data.get('num_pages', 0),
            'media_id': media_id,
            'page_urls': page_urls
        }
        
        # 5. DOM Extraction for Recommendations
        soup = BeautifulSoup(response.text, 'html.parser')
        recommendations = []
        related_container = soup.find('div', id='related-container')

        if related_container:
            galleries = related_container.find_all('div', class_='gallery')
            for gallery in galleries:
                link_tag = gallery.find('a', class_='cover')
                if not link_tag:
                    continue
                    
                href = link_tag.get('href', '')
                rec_id = href.strip('/').split('/')[-1] 
                
                caption_tag = gallery.find('div', class_='caption')
                rec_title = caption_tag.text.strip() if caption_tag else "Unknown Title"
                
                img_tag = gallery.find('img')
                thumbnail_url = None
                if img_tag:
                    thumbnail_url = img_tag.get('data-src') or img_tag.get('src')
                    if thumbnail_url and thumbnail_url.startswith('//'):
                        thumbnail_url = f"https:{thumbnail_url}"
                
                if rec_id.isdigit():
                    recommendations.append({
                        'id': int(rec_id),
                        'title': rec_title,
                        'thumbnail_image': thumbnail_url
                    })

        data_payload['recommendations'] = recommendations

        cover_div = soup.find('div', id='cover')
        if cover_div:
            cover_img = cover_div.find('img')
            if cover_img and 'src' in cover_img.attrs:
                data_payload['cover_image'] = cover_img.get('data-src') or cover_img.get('src')

        return data_payload
    
    except Exception as e:
        return {"Error": str(e)}


@app.get("/")
async def home():
    return  {"Message":"Go To The EndPoint Moron /manga_id=id_number or /docs for swagger fastapi documentation"}


@app.get("/manga_id={manga_id}")
async def getData(manga_id:int):
    return await getManga(manga_id)
