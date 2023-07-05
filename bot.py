from pyrogram import Client, filters
from pyrogram.types import Message
from re import findall as refindall,compile as recompile
from json import load
from os.path import exists

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
    SYMBOLS = load(f)

if not exists('sub.json'):
    import __get_sub
    del __get_sub
with open('sub.json','r',encoding='utf-8') as f:
    SUB = load(f)

if not exists('symbols.json'):
    import __get_super
    del __get_super
with open('super.json','r',encoding='utf-8') as f:
    SUP = load(f)

del f, exists

math_check = recompile(r'\$(?:.*)\$')
math_ambient = recompile(r'\$(?:[^\$]*)\$')
math_sub = recompile(r'_(?:\{.*\}|.)')
math_sup = recompile(r'\^(?:\{.*\}|.)')

@app.on_message(filters.me & (filters.text | filters.caption) & filters.regex(math_check))
async def math(client,message:Message):
    m = (message.text if message.text else message.caption)

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
                    for c in SUB:
                        if c.startswith('\\') and c in t_sub:
                            t_sub = t_sub.replace(c,SUB[c])
                for c in SUB:
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
                    for c in SUP:
                        if c.startswith('\\') and c in t_sup:
                            t_sup = t_sup.replace(c,SUP[c])
                for c in SUP:
                    if (not c.startswith('\\')) and c in t_sup:
                        t_sup = t_sup.replace(c,SUP[c])
                answer = answer.replace(f_sup,t_sup,1)

            if '\\' in answer:
                for c in SYMBOLS:
                    if c.startswith('\\') and c in answer:
                        answer = answer.replace(c,SYMBOLS[c])
            for c in SYMBOLS:
                if not c.startswith('\\') and c in answer:
                    answer = answer.replace(c,SYMBOLS[c])

            m = m.replace(result,answer,1)

        except:
            m = m.replace(result,result.strip('$'),1)

    await message.edit_text(m)

app.run()