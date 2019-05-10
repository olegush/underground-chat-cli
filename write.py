import os
import argparse
from datetime import datetime
import logging
import json
import asyncio

from dotenv import load_dotenv


def get_args(host_default, port_default, token_default, username_default, message_default):
    '''Parses arguments from CLI.'''
    parser = argparse.ArgumentParser(description='Undergroung Chat CLI')
    parser.add_argument('--host', help='Host', type=str)
    parser.add_argument('--port', help='Port', type=int)
    group = parser.add_mutually_exclusive_group()
    group.add_argument('--token', help='Token', type=str)
    group.add_argument('--username', help='Username', type=str)
    parser.add_argument('--message', help='Message', type=str)
    args = parser.parse_args()
    if args.username:
        token_default = None
    if args.token:
        username_default = None
    parser.set_defaults(
        host=host_default,
        port=port_default,
        token=token_default,
        username=username_default,
        message=message_default
        )
    args = parser.parse_args()
    return vars(args)


async def authorize(host, port, token, username, message):
    '''Authorizes a user and calls a submit_message() if user exists
     or calls register().'''

    try:
        reader, writer = await asyncio.open_connection(host, port)
        data = await reader.readline()
        logging.info('Received: {}'.format(data.decode()))
        writer.write('{}\n'.format(token).encode())
        logging.info('Sent token: {}'.format(token))
        data = await reader.readline()
        data_json = json.loads(data.decode())

        if data_json:
            logging.info('Received: {}'.format(data_json))
            await submit_message(reader, writer, message)
        elif username:
            logging.info('Go to register with username {}.'.format(username))
            await register(reader, writer, username)
            await submit_message(reader, writer, message)
        else:
            logging.info('Invalid token {}. Please check it.'.format(token))

    finally:
        writer.close()


async def register(reader, writer, username):
    '''Registers a new user in the chat and call submit_message().'''
    data = await reader.readline()
    logging.info(data.decode())
    writer.write('{}\n'.format(sanitize(username)).encode())
    data = await reader.readline()
    token = json.loads(data.decode())['account_hash']
    logging.info('Username "{}" registered with token {}.'.format(
        sanitize(username),
        token
        ))


def sanitize(text):
    return text.replace('\n', '').replace('\r', '')


async def submit_message(reader, writer, message):
    '''Submits a message to the chat.'''
    data = await reader.readline()
    logging.info('Received: {}'.format(data.decode()))
    message = '{}\n\n'.format(sanitize(message)).encode()
    writer.write(message)
    logging.info('Sent message: {}'.format(message.decode()))


if __name__ == '__main__':

    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s,%(msecs)d %(levelname)s: %(message)s',
        datefmt='%H:%M:%S',
        )

    load_dotenv()
    args = get_args(
            os.getenv('HOST'),
            os.getenv('PORT_WRITE'),
            os.getenv('TOKEN'),
            os.getenv('USERNAME'),
            os.getenv('MESSAGE')
            )

    loop = asyncio.get_event_loop()
    loop.run_until_complete(authorize(**args))
    loop.close()
