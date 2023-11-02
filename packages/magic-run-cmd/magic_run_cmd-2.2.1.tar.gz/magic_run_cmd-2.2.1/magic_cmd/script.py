from __future__ import annotations
from typing import (
                    Union, 
                    Callable, 
)
from pathlib import Path
from magic_cmd.engine import Engine 
from magic_cmd.run_cmd import Shell


class Script():
    
    '''
        Allows you write bash scripts in python code.
        script = Scripts()
        script.cmds = """
                        ls
                        echo "an"
                       """
        script()
    '''
    
    def __init__(self,
                 cmds:str='',
                 name:str= 'script',
                 engine:Engine=Shell(),
                ):
        self.cmds:str = cmds
        self.engine:Engine = engine
        self.name:str = name

    def __add__(self,cmd: Union[Script,str])->str:
        match(cmd):
            case str(): cmd = self.engine.clean(cmd)
            case Script() if self.engine.__class__!=cmd.engine.__class__: 
                raise Exception(f'{cmd.engine.__class__} does not match{self.engine.__class__}')
            case Script(): cmd = cmd.cmds
        return Script('\n'.join([self.cmds,cmd]))
    
    def __iadd__(self,cmd: Union[Script,str])->Script:
        return (self:=self + cmd)
    
    def __repr__(self) -> str:
        return self.cmds
    
    def __str__(self) -> str:
        return self.cmds
     
    def __call__(self,
                 lazy:bool=False,
                 name:str='lazy',
                 split:bool='False',
                 *args,**kwargs) -> Union[Path,list[str]]:
        if lazy:
            return self.engine.write(self.cmds,name=name)
        return self.engine.run(self.cmds,split=split)
        

    def append(self,cmd:Union[Script,str])->None:
        self.cmds += cmd
        