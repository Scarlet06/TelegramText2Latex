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
math_sub = recompile(r'_(?:\{[^_^]+\}|[^{])')
math_sup = recompile(r'\^(?:\{[^_^]+\}|[^{])')
   

@app.on_message(filters.me & (filters.text | filters.caption) & filters.regex(recompile(r'\$(?:.*)\$')))
async def latex(client:Client,message:Message):

    m = message.text if message.text else message.caption
    start = t = 0
    while start<len(m):

        for result in math_ambient.finditer(m,t):
            start,end = result.regs[0]
            break
        else:
            break
        current = m[start:end].strip('$')

        for sub_findet in math_sub.finditer(current):
            sub_min, sub_max = sub_findet.regs[0]
            break
        else:
            sub_min = sub_max = end
        for sup_findet in math_sup.finditer(current):
            sup_min, sup_max = sup_findet.regs[0]
            break
        else:
            sup_min = sup_max = end

        while (sub_min<end) or (sup_min<end):
            if (sub_min < sup_min and sup_max < sub_max) or (sup_max <= sub_min):

                actual = current[sup_min:sup_max]

                if actual.endswith('}'):
                    actual = actual[2:-1]
                else:
                    actual = actual[1:]

                if '\\' in actual:
                    for c in KEY_SUP:
                        if c.startswith('\\') and c in actual:
                            actual = actual.replace(c,SUP[c])
                for c in KEY_SUP:
                    if (not c.startswith('\\')) and c in actual:
                        actual = actual.replace(c,SUP[c])
                
                tt = sup_max - len(current)
                current = current.replace(current[sup_min:sup_max],actual,1)
                tt+=len(current)
            
            elif (sup_min < sub_min and sub_max < sup_max) or (sub_max <= sup_min):

                actual = current[sub_min:sub_max]

                if actual.endswith('}'):
                    actual = actual[2:-1]
                else:
                    actual = actual[1:]

                if '\\' in actual:
                    for c in KEY_SUB:
                        if c.startswith('\\') and c in actual:
                            actual = actual.replace(c,SUB[c])
                for c in KEY_SUB:
                    if (not c.startswith('\\')) and c in actual:
                        actual = actual.replace(c,SUB[c])

                tt = sub_max - len(current)
                current = current.replace(current[sub_min:sub_max],actual,1)
                tt+=len(current)
            
            else:
                break

            for sub_findet in math_sub.finditer(current,tt):
                sub_min, sub_max = sub_findet.regs[0]
                break
            else:
                sub_min = sub_max = end
            
            for sup_findet in math_sup.finditer(current,tt):
                sup_min, sup_max = sup_findet.regs[0]
                break
            else:
                sup_min = sup_max = end

        if '\\' in current:
            for c in KEY_SYMBOLS:
                if c.startswith('\\') and c in current:
                    current = current.replace(c,SYMBOLS[c])
        for c in KEY_SYMBOLS:
            if (not c.startswith('\\')) and c in current:
                current = current.replace(c,SYMBOLS[c])

        t = end - len(m)
        m = m.replace(m[start:end],current,1)
        t += len(m)
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