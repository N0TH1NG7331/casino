import asyncio
import core.core as core

if __name__ == "__main__":
    print("[DEBUG] Setuping core...")
    try:
        asyncio.run(core.setup())
    except Exception as err:
        print("[ERROR]", err)
