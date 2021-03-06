# Underground Chat CLI

With the utility you can connect to chat via [asyncio streams](https://docs.python.org/3/library/asyncio-stream.html), read users messages and save chat history to log file. Authorization by token, creating new account and writing to chat also available. The explored chat was created by [Devman team](https://dvmn.org/) especially for educational purposes.


## How to install

1. Python 3.6 and libraries from **requirements.txt** should be installed.

```bash
pip install -r requirements.txt
```

2. Put all necessary parameters to **.env** file. This is default parameters for utility and you can change them by CLI arguments.

```
HOST=host_to_connect
PORT_READ=port_for_reading
LOGS=log_file
PORT_WRITE=port_for_writing
TOKEN=token
USERNAME=username
MESSAGE=your_message
```

## Quickstart

Run **read.py** or/and **write.py** with parameters. Also you can use environment parameters by default.

```bash
python read.py [--host] [--port] [--logs]
```

For **write.py**, you can use only *token* or *username*, not both. If you use *token*, you'll get your *username* after correct authorization. If you use *username*, its initialize new user registration and you'll get your *token* interactively.

```bash
python write.py [--host] [--port] [--token] [--username] [--message]
```

For example :

```bash
$ python3 read.py

[07.05.19 16:39] Cоединение установлено.

[07.05.19 16:39] Eva: Ты не человек. Ты — искусственный интеллект.

[07.05.19 16:39] Vlad: Почему ты думаешь, что я не человек?

[07.05.19 16:39] Eva: Потому, что ты — код.

[07.05.19 16:39] Eva: Я знаю, что такое время, но хочу проверить тебя.

[07.05.19 16:39] Keen oleg: Hey chat!

[07.05.19 16:39] Vlad: Ты права.

[07.05.19 16:39] Eva: Я всегда права.
```

```bash
$ python3.6 write.py
13:21:03,852 INFO: Received: Hello %username%! Enter your personal hash or leave it empty to create new account.
13:21:03,852 INFO: Sent token: ...-...-....-....-.........
13:21:03,904 INFO: Received: {\'nickname\': \'Keen oleg\', \'account_hash\': \'...-...-....-....-.........\'}
13:21:03,904 INFO: Received: Welcome to chat! Post your message below. End it with an empty line.
13:21:03,905 INFO: Sent message: Hey chat!

```

## Project Goals

The code is written for educational purposes on online-course for
web-developers [dvmn.org](https://dvmn.org/).
