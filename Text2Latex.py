# This file is part of TelegramText2Latex.

# TelegramText2Latex is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# TelegramText2Latex is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.

# You should have received a copy of the GNU Lesser General Public License
# along with TelegramText2Latex.  If not, see <http://www.gnu.org/licenses/>.

from pyrogram import Client, filters, enums
from pyrogram.session import Session
from pyrogram.types import Message

class Bot(Client):
    # It doesn't do much. It just adds the latex method when the object is initialized
    # the latex method searches a latex math ambient (between two dollar sign) and sobstitutes the latex commands with the known corrispective unicode characters.

    def __init__(self, name: str, api_id: int | str = None, api_hash: str = None, app_version: str = Client.APP_VERSION, device_model: str = Client.DEVICE_MODEL, system_version: str = Client.SYSTEM_VERSION, lang_code: str = Client.LANG_CODE, ipv6: bool = False, proxy: dict = None, test_mode: bool = False, bot_token: str = None, session_string: str = None, in_memory: bool = None, phone_number: str = None, phone_code: str = None, password: str = None, workers: int = Client.WORKERS, workdir: str = Client.WORKDIR, plugins: dict = None, parse_mode: enums.ParseMode = enums.ParseMode.DEFAULT, no_updates: bool = None, takeout: bool = None, sleep_threshold: int = Session.SLEEP_THRESHOLD, hide_password: bool = False, max_concurrent_transmissions: int = Client.MAX_CONCURRENT_TRANSMISSIONS, filter_Latex_Ambient:filters.Filter = None) -> None:
        # It exactly is the Client.__init__ but with the 'filter_Latex_Ambient' argument, if None it will be used the deafult, which is: filters.me & (filters.text | filters.caption) & filters.regex(recompile(r'\$(?:.*)\$')

        super().__init__(name, api_id, api_hash, app_version, device_model, system_version, lang_code, ipv6, proxy, test_mode, bot_token, session_string, in_memory, phone_number, phone_code, password, workers, workdir, plugins, parse_mode, no_updates, takeout, sleep_threshold, hide_password, max_concurrent_transmissions)

        from re import compile as recompile
        from json import load
        from os.path import exists

        # it searches the normal symbols
        if not exists('symbols.json'):
            import __get_symbols
            del __get_symbols
        with open('symbols.json','r',encoding='utf-8') as f:
            SYMBOLS:dict = load(f)
            KEY_SYMBOLS:tuple[str] = tuple(sorted(SYMBOLS.keys(),key=len,reverse=True))

        # it searches the symbols for subscripted text
        if not exists('sub.json'):
            import __get_sub
            del __get_sub
        with open('sub.json','r',encoding='utf-8') as f:
            SUB:dict = load(f)
            KEY_SUB:tuple[str] = tuple(sorted(SUB.keys(),key=len,reverse=True))

        # it searches the symbols for superscripted text
        if not exists('super.json'):
            import __get_super
            del __get_super
        with open('super.json','r',encoding='utf-8') as f:
            SUP:dict = load(f)
            KEY_SUP:tuple[str] = tuple(sorted(SUP.keys(),key=len,reverse=True))

        # regex compiled to search: 
        math_ambient = recompile(r'\$(?:[^\$]+)\$') # math ambient between two dollar sign
        math_sub = recompile(r'_(?:\{[^_^]+\}|[^{])') # a subscripted text as _{12} or _2
        math_sup = recompile(r'\^(?:\{[^_^]+\}|[^{])') # a superscripted text as ^{12} or ^2

        if filter_Latex_Ambient is None:
            filter_Latex_Ambient = filters.me & (filters.text | filters.caption) & filters.regex(recompile(r'\$(?:.*)\$'))

        @self.on_message(filter_Latex_Ambient)
        async def latex(client:Client,message:Message) -> None:
            # it check for a message and tries to find any nown charaters that replaces latex commands

            # the text to edit
            m = message.text if message.text else message.caption

            #these are used to know the current "lecture position"
            start = t = 0

            while start<len(m):

                # It searches for math ambient, if none is found, the procedure is stopped
                for result in math_ambient.finditer(m,t):
                    start,end = result.regs[0]
                    break
                else:

                    break

                # it extract the amth text from the math ambient
                current = m[start:end].strip('$')

                # it search the first occourence for subscription or superscription -> the first will be edited
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

                # while there are characters in superscription or subscription to edit, this cycle will continue toedit and search for those
                while (sub_min<end) or (sup_min<end):

                    # if superscription text comes before subscription, it edits it first, else the other way around.
                    # just to be sure if none came first -> it impossible and exit the loop
                    if (sub_min < sup_min and sup_max < sub_max) or (sup_max <= sub_min):

                        # the exact text to edit
                        actual = current[sup_min:sup_max]
                        if actual.endswith('}'):
                            actual = actual[2:-1]
                        else:
                            actual = actual[1:]

                        # it replaces all the characters from the longst to the shortest
                        for c in KEY_SUP:
                            if c in actual:
                                actual = actual.replace(c,SUP[c])
                        
                        # it replaces the main section with the new one
                        tt = sup_max - len(current)
                        current = current.replace(current[sup_min:sup_max],actual,1)
                        tt+=len(current)
                    
                    elif (sup_min < sub_min and sub_max < sup_max) or (sub_max <= sup_min):

                        # the exact text to edit
                        actual = current[sub_min:sub_max]
                        if actual.endswith('}'):
                            actual = actual[2:-1]
                        else:
                            actual = actual[1:]

                        # it replaces all the characters from the longst to the shortest
                        for c in KEY_SUB:
                            if c in actual:
                                actual = actual.replace(c,SUB[c])

                        # it replaces the main section with the new one
                        tt = sub_max - len(current)
                        current = current.replace(current[sub_min:sub_max],actual,1)
                        tt+=len(current)
                    
                    else:
                        break

                    #it now searches for new subscripted or superscripted text
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

                # now it replaces each command that is neither a superscripted or subscripted text
                for c in KEY_SYMBOLS:
                    if c in current:
                        current = current.replace(c,SYMBOLS[c])

                # now it replaces the current section with what we got this far
                t = end - len(m)
                m = m.replace(m[start:end],current,1)
                t += len(m)

                # it continues this loop until no other math ambients are found

            #it finally edits the message
            await message.edit_text(m)