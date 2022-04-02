from datetime import datetime
import json
import time 
from telethon import TelegramClient
import asyncio
from telethon.tl.functions.channels import InviteToChannelRequest
from telethon.errors import PeerFloodError, UserPrivacyRestrictedError, FloodWaitError, UserChannelsTooMuchError, ChannelPrivateError, PhoneNumberBannedError
import pytz

config = json.load(open('config.json'))
clients = config['ACCOUNTS']
utc=pytz.UTC
print("Auto Invite ")
print("1. Kualitas")
print("2. Kuantitas")
choice = input("Masukkan pilihan invite: ")

async def main():
    for clientcfg in clients :
        try : 
            client =  TelegramClient(session=clientcfg['SESSION_ID'], api_id=clientcfg['APP_ID'], api_hash=clientcfg['APP_HASH_ID'])
            await client.start()
            members = json.load(open('user/' + clientcfg['PHONE_NUMBER'] + '.json'))
            # entity = await client.get_entity(int(config['FROM_GROUP']))
            last_online = utc.localize(datetime.strptime(config["LAST_ONLINE"], "%d/%m/%y %H:%M"))
            for member in members[config['FROM_GROUP']] :
                if member['username'] != None : 
                    try :
                        to = await client.get_entity(int(config['TO_GROUP']))
                        mEntity = await client.get_entity(member['username'])
                        if mEntity.bot == False : 
                            try : 
                                if choice == "1" :
                                    if (mEntity.status.was_online >= last_online)  :
                                        await client(InviteToChannelRequest(to, [mEntity]))
                                        print("Success adding " + mEntity.username + " to target group")
                                    time.sleep(30)
                                elif choice == "2" :
                                    if (mEntity.status.was_online <= last_online)  :
                                        await client(InviteToChannelRequest(to, [mEntity]))
                                        print("Success adding " + mEntity.username + " to target group")
                                    time.sleep(30)
                            except ValueError: 
                                print("No user has username " + mEntity.username )
                                continue;
                            except AttributeError : 
                                if choice == "1" :
                                    print("cannot add " + mEntity.username + " due inactivity")
                                    continue
                                elif choice == "2" :
                                    await client(InviteToChannelRequest(to, [mEntity]))
                                    print("Success adding " + mEntity.username + " to target group")
                                time.sleep(30)
                        else : 
                            print("cant invite because its a bot")
                            continue
                    except UserPrivacyRestrictedError:
                        print("cannot add " + mEntity.username + " due their privacy setting")
                        continue; 
                    except PeerFloodError as e: 
                        print("Account limited changing to next account (if exist)")
                        break
                    except UserChannelsTooMuchError: 
                        print("cannot add " + mEntity.username + " due too much group/channel")
                        continue
                    except FloodWaitError as e : 
                        print("account limit for " + e.seconds +", changing next account (if exist)")
                        time.sleep(e.seconds)
                    except ChannelPrivateError : 
                        print("account get banned or you dont have permission to see this group, changing to next account (if exist) ")
                        break;
                    
                    # print(result)
                    time.sleep(15)
        except PhoneNumberBannedError : 
            print("account get banned, changing to next account (if exist) ")
            break;

loop = asyncio.get_event_loop()
loop.run_until_complete(main())