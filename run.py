from RGBRemoteService import RGBRemoteService
import asyncio
                    

async def main():
    await RGBRemote.InitAsync()

RGBRemote = RGBRemoteService()
asyncio.run(main())