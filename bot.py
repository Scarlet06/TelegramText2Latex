from pyrogram import Client, filters, enums
from pyrogram.types import Message

from re import compile as recompile
from json import load
from os.path import exists
from datetime import timedelta

from Commands import Commands
commands = Commands()
del Commands

api_id:int
api_hash:str
with open('.env','rb') as env:
    exec(env.read())
del env

app = Client("Magic DSDP",api_id,api_hash,'1.0 alpha')
del api_id,api_hash

if not exists('symbols.json'):
    import __get_symbols
    del __get_symbols
with open('symbols.json','r',encoding='utf-8') as f:
    SYMBOLS:dict = load(f)
    KEY_SYMBOLS:tuple[str] = tuple(sorted(SYMBOLS.keys(),key=len,reverse=True))

if not exists('sub.json'):
    import __get_sub
    del __get_sub
with open('sub.json','r',encoding='utf-8') as f:
    SUB:dict = load(f)
    KEY_SUB:tuple[str] = tuple(sorted(SUB.keys(),key=len,reverse=True))

if not exists('super.json'):
    import __get_super
    del __get_super
with open('super.json','r',encoding='utf-8') as f:
    SUP:dict = load(f)
    KEY_SUP:tuple[str] = tuple(sorted(SUP.keys(),key=len,reverse=True))

del exists

math_ambient = recompile(r'\$(?:[^\$]+)\$')
math_sub = recompile(r'_(?:\{.*\}|.)')
math_sup = recompile(r'\^(?:\{.*\}|.)')
   

@app.on_message(filters.me & (filters.text | filters.caption) & filters.regex(recompile(r'\$(?:.*)\$')))
async def math(client:Client,message:Message):

    m = message.text if message.text else message.caption

    math_ambient.findall(m)
    for result in math_ambient.findall(m):

        try:

            answer = result.strip('$')

            #searching subscript
            for f_sub in math_sub.findall(answer):
                if f_sub.endswith('}'):
                    t_sub = f_sub[2:-1]
                else:
                    t_sub = f_sub[1:]
                if '\\' in t_sub:
                    for c in KEY_SUB:
                        if c.startswith('\\') and c in t_sub:
                            t_sub = t_sub.replace(c,SUB[c])
                for c in KEY_SUB:
                    if (not c.startswith('\\')) and c in t_sub:
                        t_sub = t_sub.replace(c,SUB[c])
                answer = answer.replace(f_sub,t_sub,1)

            #searching superscript
            for f_sup in math_sup.findall(answer):
                if f_sup.endswith('}'):
                    t_sup = f_sup[2:-1]
                else:
                    t_sup = f_sup[1:]
                if '\\' in t_sup:
                    for c in KEY_SUP:
                        if c.startswith('\\') and c in t_sup:
                            t_sup = t_sup.replace(c,SUP[c])
                for c in KEY_SUP:
                    if (not c.startswith('\\')) and c in t_sup:
                        t_sup = t_sup.replace(c,SUP[c])
                answer = answer.replace(f_sup,t_sup,1)

            if '\\' in answer:
                for c in KEY_SYMBOLS:
                    if c.startswith('\\') and c in answer:
                        answer = answer.replace(c,SYMBOLS[c])
            for c in KEY_SYMBOLS:
                if not c.startswith('\\') and c in answer:
                    answer = answer.replace(c,SYMBOLS[c])

            m = m.replace(result,answer,1)

        except:
            m = m.replace(result,result.strip('$'),1)

    await message.edit_text(m)

@app.on_message(filters.me & filters.text & filters.reply & filters.command('add'))
async def add(client:Client,message:Message):
    if message.reply_to_message is None:
        return await message.reply_text('Remember to replay a message to make it work.')
    
    elif len(message.command)==1:
        return await message.reply_text('Add a way to recognise the text.')
    
    commands[message.text.split(maxsplit=1)[1].lower()] = message.chat.id,message.reply_to_message_id

    await message.reply_text('Command added successfully.')

@app.on_message(filters.me & filters.text & filters.command(['del','delete','remove']))
async def delete(client:Client,message:Message):
    if len(message.command)==1:
        return await message.reply_text('Add the command you want to delete.')
    
    m = message.text.split(maxsplit=1)[1]
    if m in commands:
        del commands[m]
        return await message.reply_text('Command removed successfully.')
    await message.reply_text('Command nver added.')

@app.on_message(filters.me & filters.text & filters.command('list'))
async def listed(client:Client,message:Message):
    if commands:
        await message.reply_text("\n".join(commands.keys()))

@app.on_message((filters.private | filters.me) & filters.text & filters.command(['remind','reminder']))
async def remind(client:Client,message:Message):

    characters = '0123456789()+/*-'

    if len(message.command)==1:
        return await message.reply_text('Use `/remind <min> <what>` to remind what in min minutes.',parse_mode=enums.ParseMode.MARKDOWN)
    
    elif len(message.command) == 2:
        if message.reply_to_message is None:
            return await message.reply_text('If you use `/remind <min> <what>` without a what, just replay a message to remind it.',parse_mode=enums.ParseMode.MARKDOWN)
        
        elif all(x in characters for x in message.command[1]):
            await message.reply_text('Reminder setted')
            return await message.reply_to_message.forward(message.chat.id,schedule_date=message.date+timedelta(minutes=eval(message.command[1])))
        
        return await message.reply_text('Using `/remind <min> <what>` remember to set min as minutes.',parse_mode=enums.ParseMode.MARKDOWN)
    
    elif all(x in characters for x in message.command[1]):
        await message.reply_text('Reminder setted')
        return await message.reply_text(' '.join(message.command[2:]),schedule_date=message.date+timedelta(minutes=eval(message.command[1])))
    
    return await message.reply_text('Using `/remind <min> <what>` remember to set min as minutes.',parse_mode=enums.ParseMode.MARKDOWN)

async def find(flt, client:Client, query:Message):
    return (query.text if query.text else query.caption).lower() in commands

@app.on_message(filters.me & (filters.text | filters.caption) & filters.create(find))
async def call(client:Client, message:Message):

    if message.chat.type.value == message.chat.type.BOT.value:
        return

    m = (message.text if message.text else message.caption).lower()
    replay_id = None
    if message.reply_to_message:
        replay_id = message.reply_to_message.id
    try:
        await message.delete()
        await client.copy_message(message.chat.id,*commands[m],reply_to_message_id=replay_id)
        # await client.forward_messages(message.chat.id,*commands[m])
    except:
        del commands[m]
        await message.reply_text(f'message not found, command {m} removed',reply_to_message_id=replay_id)

print('start')
app.run()