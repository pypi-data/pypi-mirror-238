from UVANewsApiModule import UVA_news_api as u_api
import asyncio

async def main():
  print(await u_api.get_recent(1))

asyncio.run(main())