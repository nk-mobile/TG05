# bot/api.py
import aiohttp
from typing import Optional, Dict
from bot.config import THE_DOG_API_KEY

BASE_URL = "https://api.thedogapi.com/v1"  # ✅ Без пробелов!
HEADERS = {"x-api-key": THE_DOG_API_KEY}


async def get_all_dog_breeds() -> list[Dict]:
    """Получает все породы собак (для поиска по имени)"""
    async with aiohttp.ClientSession() as session:
        async with session.get(f"{BASE_URL}/breeds", headers=HEADERS) as response:
            if response.status == 200:
                return await response.json()
            return []


async def get_breed_info(breed_name: str) -> Optional[Dict]:
    """Находит породу по точному совпадению имени (без учёта регистра)"""
    breeds = await get_all_dog_breeds()
    for breed in breeds:
        if breed["name"].lower() == breed_name.lower():
            return breed
    return None


async def get_image_by_breed_id(breed_id: int) -> Optional[str]:
    """Получает URL изображения по ID породы"""
    async with aiohttp.ClientSession() as session:
        async with session.get(
            f"{BASE_URL}/images/search",
            params={"breed_ids": breed_id},
            headers=HEADERS
        ) as response:
            if response.status == 200:
                data = await response.json()
                if data: # ← Теперь всё корректно: условие ДО комментария
                    return data[0]["url"]
    return None