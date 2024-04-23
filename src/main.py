import asyncio
import configs
import core.core as core

if __name__ == "__main__":
    print("Select boot mode (0 - Test | 1 Normal)")
    boot_mode = input("$: ")

    if boot_mode == "0":
        pass
    elif boot_mode == "1":
        configs.BOT_TESTING = False
        configs.CHANNAL_TESTING = False
        configs.CRYPTOBOT_TESTANET = False
    else:
        print("ERROR UNKNOW BOOT MODE!")
        exit(-1)

    print("[DEBUG] Setuping core...")
    try:
        asyncio.run(core.setup())
    except Exception as err:
        print("[ERROR]", err)
