import os
import argparse
from datetime import datetime
import logging
import json

from dotenv import load_dotenv
import asyncio


def get_args(host, port, token, username, message):
    parser = argparse.ArgumentParser(description='Undergroung Chat CLI')

    parser.add_argument('--host', help='Host', type=str, default=host)
    parser.add_argument('--port', help='Port', type=int, default=port)
    group = parser.add_mutually_exclusive_group()
    group.add_argument('--token', help='Token', type=str, default=token)
    group.add_argument('--username', help='Username', type=str, default=username)
    parser.add_argument('--message', help='Message', type=str, default=message)
    args = parser.parse_args()
    return args

async def sanitize(text):
    return text.replace('\n', '').replace('\r', '')

async def register(reader, writer, username):
    data = await reader.readline()
    logging.info(data.decode())
    writer.write('{}\n'.format(await sanitize(username)).encode())
    data = await reader.readline()
    token = json.loads(data.decode())['account_hash']
    logging.info('Username "{}" registered with token {}.'.format(await sanitize(username), token))
    await submit_message(reader, writer, 'I am \n the \\ new!')


async def submit_message(reader, writer, message):
    data = await reader.readline()
    logging.info('Received: {}'.format(data))
    message = '{}\n\n'.format(await sanitize(message)).encode()
    writer.write(message)
    logging.info('Sent message: {}'.format(message.decode()))
    writer.close()


async def authorize(host, port, token, username, message):
    reader, writer = await asyncio.open_connection(host, port)
    data = await reader.readline()
    logging.info('Received: {}'.format(data))
    writer.write('{}\n'.format(token).encode())
    logging.info('Sent token: {}'.format(token))
    data = await reader.readline()
    data_json = json.loads(data.decode())

    if data_json:
        logging.info('Received: {}'.format(data_json))
        await submit_message(reader, writer, message)
    elif username:
        logging.info('Invalid token but not empty username. Go to register.')
        await register(reader, writer, username)
    else:
        logging.info('Invalid token and empty username. Check it and run again.')


if __name__ == '__main__':

    load_dotenv()
    args = get_args(
            os.getenv('HOST'),
            os.getenv('PORT_WRITE'),
            os.getenv('TOKEN'),
            os.getenv('USERNAME'),
            os.getenv('MESSAGE')
            )
    host, port, token, username, message = args.host, args.port, args.token, args.username, args.message

    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s,%(msecs)d %(levelname)s: %(message)s',
        datefmt='%H:%M:%S',
        )

    loop = asyncio.get_event_loop()
    loop.run_until_complete(authorize(host, port, token, username, message))
    loop.close()