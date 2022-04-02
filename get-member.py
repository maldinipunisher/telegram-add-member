import json
import time
from telethon import TelegramClient
from telethon.errors import MultiError
import asyncio
import pytz
from datetime import datetime

config = json.load(open('config.json'))
clients = config['ACCOUNTS']
utc=pytz.UTC

print("Auto Invite ")
print("1. Kualitas")
print("2. Kuantitas")
choice = input("Masukkan pilihan invite: ")

async def main():
    for clientcfg in clients :
        client =  TelegramClient(session=clientcfg['SESSION_ID'], api_id=clientcfg['APP_ID'], api_hash=clientcfg['APP_HASH_ID'])
        await client.start()
        path = 'user/' + clientcfg['PHONE_NUMBER'] + '.json'
        # groups = json.load(open('group/' + clientcfg['PHONE_NUMBER'] + '.json'))
        data = {}
        user = [] 
        entity = await client.get_entity(int(config['FROM_GROUP']))
        participants = await client.get_participants(entity,limit=3000, aggressive=True)
        for participant in participants: 
            last_online = utc.localize(datetime.strptime(config["LAST_ONLINE"], "%d/%m/%y %H:%M"))
            if choice == "1" : 
                if hasattr(participant.status, "expires") : 
                    if participant.status.expires > last_online : 
                        user.append({'uid' :  participant.id, 'first_name' : participant.first_name ,'last_name' : participant.last_name, 'username' : participant.username, 'last_online' : participant.status.expires.strftime("%d/%m/%y %H:%S")})
                    else : 
                        continue
            else :
                if hasattr(participant.status, "expires") : 
                    if participant.status.expires < last_online : 
                        user.append({'uid' :  participant.id, 'first_name' : participant.first_name ,'last_name' : participant.last_name, 'username' : participant.username, 'last_online' : participant.status.expires.strftime("%d/%m/%y %H:%S")})
                    else : 
                        continue
                else : 
                    user.append({'uid' :  participant.id, 'first_name' : participant.first_name ,'last_name' : participant.last_name, 'username' : participant.username, 'last_online' : "Long time ago"})
            # print(participant.status.expires)
            # break
        data[config['FROM_GROUP']] = user
        try: 
            with open(path, 'w') as f : 
               f.write(json.dumps(data))
            print('success dump user from group')
        except PermissionError: 
            print('error cant create new file')
            

loop = asyncio.get_event_loop()
loop.run_until_complete(main())