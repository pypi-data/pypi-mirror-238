from typing import Union,NamedTuple 
from pathlib import Path
from subprocess import Popen, PIPE as l
from pysimplelog import Logger
from inspect import getframeinfo, currentframe
from paramiko import SSHClient, AutoAddPolicy
from json import dumps
logger = Logger(__name__)
logger.set_log_file_basename('run_cmd')
logger.set_minimum_level(logger.logLevels['info'])

know_host = Path.home()/'.ssh/known_hosts'

def run_cmd(cmd:str, split:bool=False) -> Union[list[str],str]:
    """
    A simple wrapper for Popon to run shell commands from python
    
    Args:
        cmd str: The comanda you want to run
        example: ls
    Raises:
        OSError: If the command throws an error this  captures it. 
        example: ls /does_not_exist
    Returns:
        List[str] or str: This is output of the cmd, either as a string or
        as list which is the string spilt on endline.
    """    
    
    debug_msg = f"""########
                  {getframeinfo(currentframe())=}
                  {cmd=}{type(cmd)=}
                  {split=}{type(split)=}"""
    logger.debug(debug_msg)
    
    out, err = Popen(cmd,shell=True,stdout=l).communicate()
    debug_msg = f"""What is {out=}?
                    What is {err=}?"""
    logger.debug(debug_msg)
    
    if err:
        error_msg = f"""There was an error:
                        {err}
                        """
        logger.error(error_msg, stack_info= True)
        raise OSError(err)
    return [o for o in out.decode().split('\n') if o] if split else out.decode()

def clean_cmd(cmds:Union[list[str],str]) -> str:
    match(cmds):
        case str():
            cmds:list[str] = [cmd for cmd in cmds.split('\n') if cmd]
        case list():
            cmds=cmds
    return '\n'.join([cmd.strip() for cmd in cmds])
class Shell():
    
    def run(self,cmds:str,split:bool):
        commmand_list: list[str] = cmds.split('\n')
        commmand_list = [cmd.strip() for cmd in commmand_list if cmd]
        return [run_cmd(cmd,split=split) for cmd in commmand_list]
    
    def write(self,cmds:str,name:str='shell') -> Path:
        (file_:=Path(name+'.sh')).write_text(cmds)
        return file_
    
    def clean(self,cmds:str) -> str:
        return clean_cmd(cmds)
    
class SSH_Connection(NamedTuple):
    ip: str
    key_file: str
    username: str

def run_ssh_cmd(cmd:str,
                connection:SSH_Connection, 
                split:bool=False
                ) -> tuple[str, str]:
    ip, key_file, username = connection
    client = SSHClient()
    client.load_host_keys(know_host.as_posix())
    client.set_missing_host_key_policy(AutoAddPolicy())
    client.connect(ip,username=username, key_filename=key_file)
    _, out, err = client.exec_command(cmd)
    out:str = out.read().decode()
    err:str = err.read().decode()
    if err:
        error_msg = f"""There was an error:
                        {err}
                        """
        logger.error(error_msg, stack_info= True)
        raise OSError(err)
    return [o for o in out.split('\n') if o] if split else out

class SSH_Shell():
    
     
    def __init__(self,connection:SSH_Connection):
        self.connection:SSH_Connection = connection
    
    
    def run(self,cmds:str,split:bool):
        commmand_list: list[str] = cmds.split('\n')
        commmand_list = [cmd.strip() for cmd in commmand_list if cmd]
        return [run_ssh_cmd(cmd,self.connection,split=split)
                for cmd in commmand_list]
    
    def write(self,cmds:str,name:str='shell') -> Path:
        (file_:=Path(name+'.sh')).write_text(dumps({
                                                'connection':self.connection
                                                ,'cmds':cmds,
                                                }))
        return file_
    
    def clean(self,cmds:str) -> str:
        return clean_cmd(cmds)