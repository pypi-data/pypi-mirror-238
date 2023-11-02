from typing import Protocol, Union

class Engine(Protocol):

    name:str
        
    def run(cmds:Union[str,list[str]],*args,**kwargs)->str:
        ...
    def write(cmds:Union[str,list[str]],*args,**kwargs)->None:
        ...
    def clean(cmds:Union[str,list[str]],*args,**kwargs)->str:
        ...

