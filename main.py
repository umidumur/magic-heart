import asyncio
from maps import*
from envar import*

from random import choice

from telethon import TelegramClient
from telethon.events import NewMessage


HEART = '🤍'
HEARTS = ['🤎','🧡','💙','🖤','💛','💜','❤️‍🔥','💚','❤️‍🩹','💖','❤']
COLORED_HEARTS = ['❤','💚','💙','💜','❤️‍🩹','❤️‍🔥','💖','💝']
MAGIC_PHRASES = ['magic','ily']
EDIT_DELAY = 0.01

PARADE_MAP = '''
000000000
001101100
011111110
011111110
011111110
001111100
000111000
000010000
000000000
'''


client = TelegramClient('tg-account', APP_ID, API_HASH)


def generate_parade_colored():
    output = ''
    for c in PARADE_MAP:
        if c == '0':
            output += HEART
        elif c == '1':
            output += choice(COLORED_HEARTS)
        else:
            output += c
    return output

def generate_parade_hearts(num):
    output = ''
    for c in PARADE_MAP:
        if c == '0':
            output += HEART
        elif c == '1':
            output += HEARTS[num]
        else:
            output += c
    return output

def generate_end(num1,num2):
    output = ''
    for c in END_MAP[num1]:
        if c == '0':
            output += HEART
        elif c == '1':
            output += HEARTS[num2]
        else:
            output += c
    return output



async def process_love_words(event: NewMessage.Event):
    await client.edit_message(event.peer_id.user_id, event.message.id, 'i')
    await asyncio.sleep(1)
    await client.edit_message(event.peer_id.user_id, event.message.id,
                              'i love')
    await asyncio.sleep(1)
    await client.edit_message(event.peer_id.user_id, event.message.id,
                              'i love you')
    await asyncio.sleep(1)
    await client.edit_message(event.peer_id.user_id, event.message.id,
                              'i love you forever')
    await asyncio.sleep(1)
    await client.edit_message(event.peer_id.user_id, event.message.id,
                              'i love you forever❤️‍🩹')
    await asyncio.sleep(1)
    await client.edit_message(event.peer_id.user_id, event.message.id,
                              '❤️')


async def process_build_place(event: NewMessage.Event):
    output = ''
    for i in range(9):
        output += 9*HEART
        output += '\n'
        await client.edit_message(event.peer_id.user_id, event.message.id, output)
        await asyncio.sleep(EDIT_DELAY / 2)


async def process_colored_heart(event: NewMessage.Event):
    output = ''
    for i in range(11):
        text = generate_parade_hearts(i)
        await client.edit_message(event.peer_id.user_id, event.message.id, text)
        await asyncio.sleep(EDIT_DELAY)

async def process_preend(event: NewMessage.Event):
    output = ''
    text = generate_parade_hearts(10)
    await client.edit_message(event.peer_id.user_id, event.message.id, text)
    await asyncio.sleep(EDIT_DELAY)


async def process_colored_parade(event: NewMessage.Event):
    for i in range(15):
        text = generate_parade_colored()
        await client.edit_message(event.peer_id.user_id, event.message.id, text)
        await asyncio.sleep(2*EDIT_DELAY)


async def process_end(event: NewMessage.Event):
    output = ''
    for i in range(11):
        for c in range(2):
            text = generate_end(c,i)        
            await client.edit_message(event.peer_id.user_id, event.message.id, text)
            await asyncio.sleep(EDIT_DELAY)


@client.on(NewMessage(outgoing=True))
async def handle_message(event: NewMessage.Event):
    if event.message.message in MAGIC_PHRASES:
        await process_build_place(event)
        await process_colored_heart(event)
        await process_colored_parade(event)
        await process_preend(event)
        await process_end(event)
        await process_love_words(event)


if __name__ == '__main__':
    print('[*] Connect to client...')
    client.start()
    client.run_until_disconnected()
