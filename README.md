
# Windows service
- python main.py install
- python main.py start
- python main.py stop
- python main.py remove

if Error installing service: The process cannot access the file because it is being used by another process. (32) run this
```
taskkill /F /FI "SERVICES eq PCWorkloadService
```