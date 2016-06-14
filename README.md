# simple-fsm
Web app evaluating deterministic finite state machines.

Python 3.5.1

Live version: Not yet available

Date of first release: 14. 6. 2016

## Before deployment:

- Create file src/conf.txt containing:

```
e-mail address
password
smtp server
```

- When deploying to a server using Python 2.7, change the line `from urllib.parse import unquote` in app.py to `from urllib import unquote`.
