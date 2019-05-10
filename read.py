import os
import argparse
from datetime import datetime
import asyncio

from dotenv import load_dotenv
from aiofile import AIOFile

DELAY_TO_CONNECT = 5


def get_args(host, port, logs):
    '''Parses arguments from CLI.'''

    parser = argparse.ArgumentParser(description='Undergroung Chat CLI')
    parser.add_argument('--host', help='Host', type=str, default=host)
    parser.add_argument('--port', help='Port', type=int, default=port)
    parser.add_argument('--logs', help='Log file', type=str, default=logs)
    args = parser.parse_args()
    return vars(args)


async def read_chat(host, port, logs):
    '''Async chat reader.'''

    reconnect = True
    async with AIOFile(logs, 'a') as afp:
        try:
            reader, writer = await asyncio.open_connection(host, port)
            while True:
                data = await reader.readline()
                if data and reconnect:
                    await write_print_log('Cоединение установлено.\n', afp)
                await write_print_log(data.decode(), afp)
                reconnect = False

        except requests.exceptions.ConnectionError:
            await write_print_log(
                'Нет соединения. Повторная'
                'попытка через {} секунд.\n'.format(DELAY_TO_CONNECT), afp)
            reconnect = True
            asyncio.sleep(DELAY_TO_CONNECT)


async def write_print_log(message, afp):
    '''Async log writer.'''

    log = '[{}] {}'.format(datetime.now().strftime('%d.%m.%y %H:%M'), message)
    await afp.write(log)
    await afp.fsync()
    print(log)


if __name__ == '__main__':
    load_dotenv()
    args = get_args(os.getenv('HOST'), os.getenv('PORT_READ'), os.getenv('LOGS'))
    loop = asyncio.get_event_loop()
    loop.run_until_complete(read_chat(**args))
    loop.close()
