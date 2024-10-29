from aiocache import Cache

from utils import parse_all_schedules

cache = Cache(Cache.MEMORY)
cache_ttl = 300


async def get_cached_schedule():
    # Проверяем наличие расписания в кэше
    cached_data = await cache.get("schedule_data")
    if cached_data is not None:
        return cached_data
    # Если данных нет в кэше, выполняем парсинг и сохраняем данные в кэш
    data = await parse_all_schedules()
    await cache.set("schedule_data", data, ttl=cache_ttl)
    return data
