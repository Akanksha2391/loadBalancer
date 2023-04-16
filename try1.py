import aiohttp
import asyncio
import json

characters = range(1,5)
base_url = 'http://localhost:8000/'
async def get_character_info(character, session):
    r = await session.request('GET', url= base_url)
    data = await r.json()
    # print(data.message)
    # print("#########################")
    return data
async def main(characters):
    async with aiohttp.ClientSession() as session:
        tasks = []
        for char in characters:
            tasks.append(get_character_info(character=char, session=session))
        results = await asyncio.gather(*tasks, return_exceptions=True)
        # print(results)
    return results
if __name__ == '__main__':
    data = asyncio.run(main(characters))
    for item in data:
        print(item)