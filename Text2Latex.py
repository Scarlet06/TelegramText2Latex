
from pyrogram import Client, filters, enums
from pyrogram.session import Session
from pyrogram.types import Message

class Bot(Client):
    def __init__(self, name: str, api_id: int | str = None, api_hash: str = None, app_version: str = Client.APP_VERSION, device_model: str = Client.DEVICE_MODEL, system_version: str = Client.SYSTEM_VERSION, lang_code: str = Client.LANG_CODE, ipv6: bool = False, proxy: dict = None, test_mode: bool = False, bot_token: str = None, session_string: str = None, in_memory: bool = None, phone_number: str = None, phone_code: str = None, password: str = None, workers: int = Client.WORKERS, workdir: str = Client.WORKDIR, plugins: dict = None, parse_mode: enums.ParseMode = enums.ParseMode.DEFAULT, no_updates: bool = None, takeout: bool = None, sleep_threshold: int = Session.SLEEP_THRESHOLD, hide_password: bool = False, max_concurrent_transmissions: int = Client.MAX_CONCURRENT_TRANSMISSIONS, filter_Latex_Ambient:filters.Filter = None):

        super().__init__(name, api_id, api_hash, app_version, device_model, system_version, lang_code, ipv6, proxy, test_mode, bot_token, session_string, in_memory, phone_number, phone_code, password, workers, workdir, plugins, parse_mode, no_updates, takeout, sleep_threshold, hide_password, max_concurrent_transmissions)

        from re import compile as recompile
        from json import load
        from os.path import exists

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

        math_ambient = recompile(r'\$(?:[^\$]+)\$')
        math_sub = recompile(r'_(?:\{[^_^]+\}|[^{])')
        math_sup = recompile(r'\^(?:\{[^_^]+\}|[^{])')

        if filter_Latex_Ambient is None:
            filter_Latex_Ambient = filters.me & (filters.text | filters.caption) & filters.regex(recompile(r'\$(?:.*)\$'))

        @self.on_message(filter_Latex_Ambient)
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
