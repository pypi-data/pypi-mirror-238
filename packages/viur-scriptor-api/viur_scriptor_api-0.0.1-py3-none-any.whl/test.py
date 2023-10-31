from viur.scriptor.dialog import table
import asyncio

async def main():
    x = await table(header=["Name", "Vorname"], rows=[["1", "2"], ['3', '4']], select=True, multiple=True)
    print(x)

asyncio.run(main())