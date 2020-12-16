'''
Created on 24 Apr 2020

@author: dkr85djo
'''
import sys


from moddem.modealgame import MDGameState
from moddem.modealdipc import MDGameIPC
import os

# make sure at this point there is a
# serialized XML card set specification

h = 'localhost'
p = 24571
b = 'serve_dir'

if 'hypolydian' in sys.argv:
    h = 'hypolydian'
elif 'ionian' in sys.argv:
    h = 'ionian'
    p = 24571

if len(sys.argv) - 1 > 1:
    p = int(sys.argv[2])
    b = sys.argv[3]
    
    
mdstat = MDGameState()
ipc = MDGameIPC(mdstat, h, p, b)

try:
    print("Starting daemon...", h, p, b)
    ipc.daemon_deploy()      
  
except KeyboardInterrupt:
    print('Server interrupted, shutting down...')
    ipc.daemon_shutdown()
    ipc.daemon_kill()            
                        
    try:
        sys.exit(0)
    except SystemExit:
        os._exit(0)
except SystemExit:
    ipc.daemon_shutdown()
    ipc.daemon_kill()
    os._exit(0)
    
