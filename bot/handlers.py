# bot/handlers.py
from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command
from bot.api import get_all_dog_breeds, get_breed_info, get_image_by_breed_id

router = Router()


@router.message(Command("start"))
async def cmd_start(message: Message):
    await message.answer(
        "🐶 Привет! Напиши название породы собаки, и я пришлю тебе её фото и описание.\n"
        "Используй /list, чтобы увидеть все доступные породы."
    )


@router.message(Command("list"))
async def cmd_list(message: Message):
    breeds = await get_all_dog_breeds()
    if not breeds:
        await message.answer("❌ Не удалось загрузить список пород. Попробуйте позже.")
        return

    # Извлекаем и сортируем названия пород
    breed_names = sorted([breed["name"] for breed in breeds])

    # Разбиваем на части, если список слишком длинный (ограничение Telegram — 4096 символов)
    chunk_size = 100  # ~100 пород на сообщение
    for i in range(0, len(breed_names), chunk_size):
        chunk = breed_names[i:i + chunk_size]
        text = "📋 Список пород собак:\n\n" + "\n".join(chunk)
        await message.answer(text)

@router.message(F.text)
async def send_dog_info(message: Message):
    breed_name = message.text.strip()

    # Ищем породу
    breed_info = await get_breed_info(breed_name)
    if not breed_info:
        await message.answer("❌ Порода не найдена. Проверь название и попробуй ещё раз.")
        return

    # Получаем фото
    image_url = await get_image_by_breed_id(breed_info["id"])
    if not image_url:
        await message.answer("🖼 К сожалению, нет фото для этой породы.")

    # Формируем описание
    info = (
        f"🐾 *{breed_info['name']}*\n\n"
        f"📝 *Описание:* {breed_info.get('temperament', 'Нет данных')}\n\n"
        f"📏 *Вес:* {breed_info.get('weight', {}).get('imperial', 'Не указан')} фунтов\n"
        f"🌍 *Происхождение:* {breed_info.get('origin', 'Неизвестно')}\n"
        f"🕒 *Продолжительность жизни:* {breed_info.get('life_span', 'Не указана')}"
    )

    # Отправляем фото с описанием
    if image_url:
        await message.answer_photo(photo=image_url, caption=info, parse_mode="Markdown")
    else:
        await message.answer(info, parse_mode="Markdown")