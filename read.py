import os
import argparse
from datetime import datetime

from dotenv import load_dotenv
import asyncio
from aiofile import AIOFile


def get_args(host, port, logs):
    parser = argparse.ArgumentParser(description='Undergroung Chat CLI')
    parser.add_argument('--host', help='Host', type=str, default=host)
    parser.add_argument('--port', help='Port', type=int, default=port)
    parser.add_argument('--logs', help='Log file', type=str,default=logs)
    args = parser.parse_args()
    return args


async def write_print_log(message, logs):
    log = '[{}] {}'.format(datetime.now().strftime('%d.%m.%y %H:%M'), message)
    async with AIOFile(logs, 'a') as afp:
        await afp.write(log)
        await afp.fsync()
    print(log)


async def read_chat(host, port, logs):
    reader, writer = await asyncio.open_connection(host, port)
    reconnect = True

    while True:
        try:
            data = await asyncio.wait_for(reader.readline(), 3)
            if data and reconnect:
                await write_print_log('Cоединение установлено.\n', logs)
            await write_print_log(data.decode(), logs)
            reconnect = False

        except asyncio.TimeoutError:
            await write_print_log('Нет соединения. Повторная попытка через 5 секунд.\n', logs)
            reconnect = True
            asyncio.sleep(5)


if __name__ == '__main__':
    load_dotenv()
    args = get_args(os.getenv('HOST'), os.getenv('PORT_READ'), os.getenv('LOGS'))
    host, port, logs = args.host, args.port, args.logs
    loop = asyncio.get_event_loop()
    loop.run_until_complete(read_chat(host, port, logs))
    loop.close()
