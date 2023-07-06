from json import load,dump

class Commands(dict):

    def __init__(self):
        from os.path import exists
        if exists('commands.json'):
            try:
                with open('commands.json') as f:
                    super().__init__(load(f))
            except:
                super().__init__()
        else:
            super().__init__()
    
    def __write(self):
        with open('commands.json','w') as f:
            dump(self,f)

    def __setitem__(self, __key, __value) -> None:
        super().__setitem__(__key, __value)
        self.__write()

    def __delitem__(self, __key) -> None:
        super().__delitem__(__key)
        self.__write()
