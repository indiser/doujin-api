from fastapi import FastAPI
import re
from bs4 import BeautifulSoup
from datetime import datetime
import json
from curl_cffi.requests import AsyncSession
from contextlib import asynccontextmanager

session = AsyncSession(impersonate="chrome")

@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    await session.close()

app=FastAPI(lifespan=lifespan)

async def getManga(id:int):
    nhentai_url=f"https://nhentai.net/g/{id}/"
    HEADERS = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    response = await session.get(url=nhentai_url,headers=HEADERS)

    try:
        if response.status_code==200:
            data_payload = {}
            json_pattern = r"window\._gallery\s*=\s*JSON\.parse\(\"(.*?)\"\);"
            match = re.search(json_pattern, response.text)
            if match:
                clean_json_str = match.group(1).encode('utf-8').decode('unicode_escape')
                gallery_data = json.loads(clean_json_str)

                media_id = gallery_data['media_id']
                pages = gallery_data['images']['pages']
                page_urls = []

                ext_map = {'j': 'jpg', 'p': 'png', 'w': 'webp', 'g': 'gif'}
                for i, page in enumerate(pages, start=1):
                    ext = ext_map.get(page['t'], 'jpg')
                    page_urls.append(f"https://i.nhentai.net/galleries/{media_id}/{i}.{ext}")

                data_payload = {
                    'id': int(gallery_data['id']),
                    'title': gallery_data['title']['english'],
                    'date': datetime.fromtimestamp(gallery_data['upload_date']).strftime('%Y-%m-%d'),
                    'parodies':[tag['name'] for tag in gallery_data['tags'] if tag['type'] == 'parody'],
                    'characters':[tag['name'] for tag in gallery_data['tags'] if tag['type'] == 'character'],
                    'groups': [tag['name'] for tag in gallery_data['tags'] if tag['type'] == 'group'],
                    'categories': [tag['name'] for tag in gallery_data['tags'] if tag['type'] == 'category'],
                    'language':[tag['name'] for tag in gallery_data['tags'] if tag['type'] == 'language'],
                    'favorites': int(gallery_data['num_favorites']),
                    'tags': [tag['name'] for tag in gallery_data['tags'] if tag['type'] == 'tag'],
                    'artists': [tag['name'] for tag in gallery_data['tags'] if tag['type'] == 'artist'],
                    'num_pages': int(gallery_data['num_pages'])
                }

                data_payload['media_id'] = media_id
                data_payload['page_urls'] = page_urls
            
            soup = BeautifulSoup(response.text, 'html.parser')
            recommendations = []
            related_container = soup.find('div', id='related-container')

            if related_container:
                for gallery in related_container.find_all('div', class_='gallery'):
                    link_tag = gallery.find('a', class_='cover')
                    caption_tag = gallery.find('div', class_='caption')
                    
                    if link_tag and caption_tag:
                        rec_id = link_tag['href'].strip('/').split('/')[-1]
                        rec_title = caption_tag.text
                        recommendations.append({'id': int(rec_id), 'title': rec_title})

            data_payload['recommendations'] = recommendations

            cover_div = soup.find('div', id='cover')
            if cover_div:
                cover_img = cover_div.find('img')
                if cover_img and 'data-src' in cover_img.attrs:
                    cover_url = "https:" + cover_img['data-src']
                    data_payload['cover_image'] = cover_url
        return data_payload
    except Exception as e:
        return {"Error":e}

@app.get("/")
async def home():
    return  {"Message":"Go To The EndPoint Moron /manga_id=id_number or /docs for swagger fastapi documentation"}


@app.get("/manga_id={manga_id}")
async def getData(manga_id:int):
    return await getManga(manga_id)
