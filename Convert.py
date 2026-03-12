##[debug]Evaluating: secrets.SESSION_STRING
##[debug]Evaluating Index:
##[debug]..Evaluating secrets:
##[debug]..=> Object
##[debug]..Evaluating String:
##[debug]..=> 'SESSION_STRING'
##[debug]=> '***'
##[debug]Result: '***'
##[debug]Evaluating: secrets.API_ID
##[debug]Evaluating Index:
##[debug]..Evaluating secrets:
##[debug]..=> Object
##[debug]..Evaluating String:
##[debug]..=> 'API_ID'
##[debug]=> '***'
##[debug]Result: '***'
##[debug]Evaluating: secrets.API_HASH
##[debug]Evaluating Index:
##[debug]..Evaluating secrets:
##[debug]..=> Object
##[debug]..Evaluating String:
##[debug]..=> 'API_HASH'
##[debug]=> '***'
##[debug]Result: '***'
##[debug]Evaluating condition for step: 'Run bot'
##[debug]Evaluating: success()
##[debug]Evaluating success:
##[debug]=> true
##[debug]Result: true
##[debug]Starting: Run bot
##[debug]Loading inputs
##[debug]Loading env
Run python bot.py
##[debug]/usr/bin/bash -e /home/runner/work/_temp/66a89910-acc6-40f9-ab0e-56d0696b6151.sh
Traceback (most recent call last):
  File "/home/runner/work/E/E/bot.py", line 23, in <module>
    client = TelegramClient(StringSession(SESSION_STRING), API_ID, API_HASH)
  File "/opt/hostedtoolcache/Python/3.9.25/x64/lib/python3.9/site-packages/telethon/sessions/string.py", line 33, in __init__
##[debug]Dropping file value '/opt/hostedtoolcache/Python/3.9.25/x64/lib/python3.9/site-packages/telethon/sessions/string.py'. Path is not under the workflow repo.
Error:     raise ValueError('Not a valid string')
ValueError: Not a valid string
Error: Process completed with exit code 1.
##[debug]Finishing: Run bot
