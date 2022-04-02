import json
import time
from telethon import TelegramClient
import asyncio

config = json.load(open('config.json'))
# client = TelegramClient(session=config['SESSION_ID'], api_id=config['APP_ID'], api_hash=config['APP_HASH_ID'])
# client.start()
# path = 'group/' + config['PHONE_NUMBER'] + '.json'

async def main():
    clients = config['ACCOUNTS']
    for clientcfg in clients :
        client =  TelegramClient(session=clientcfg['SESSION_ID'], api_id=clientcfg['APP_ID'], api_hash=clientcfg['APP_HASH_ID'])
        await client.start()
        path = 'group/' + clientcfg['PHONE_NUMBER'] + '.json'
        dialogs = await client.get_dialogs()
        data = {}
        for dialog in dialogs : 
            if dialog.is_channel :
                # print()
                if(dialog.entity.megagroup == True) :
                    data[dialog.id] = {'id' : dialog.id, 'name' : dialog.name, "type" : "GROUP"}
                else : 
                    data[dialog.id] = {'id' : dialog.id, 'name' : dialog.name, "type" : "CHANNEL"}

            with open(path, 'w') as f : 
                    try : 
                        f.write(json.dumps(data))
                        print("successfully add group to dump file")
                    except PermissionError : 
                        print('error creating new file!')
        data.clear()
        time.sleep(5)

loop = asyncio.get_event_loop()
loop.run_until_complete(main())