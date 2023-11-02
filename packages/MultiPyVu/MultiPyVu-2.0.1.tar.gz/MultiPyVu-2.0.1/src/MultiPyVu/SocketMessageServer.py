# -*- coding: utf-8 -*-
"""
SocketMessageServer inherits SocketMessage and is used by the server
to communicate with socket client via SocketMessageClient

Created on Mon Jun 7 23:47:19 2021

@author: D. Jackson
"""

import logging
from typing import Dict

from .SocketMessage import Message
from .exceptions import MultiPyVuException
from .QdCommandParser import QdCommandParser
from .project_vars import SERVER_NAME


class ServerMessage(Message):
    def __init__(self,
                 selector,
                 sock,
                 qdCommandParser: QdCommandParser,
                 verbose: bool,
                 scaffolding: bool,
                 server_threading: bool
                 ):
        super().__init__(sock)
        self.selector = selector
        self.addr = sock.getpeername()
        self.qd_command = qdCommandParser
        self.verbose = verbose
        self.scaffolding = scaffolding
        self.server_threading = server_threading
        self.logger = logging.getLogger(SERVER_NAME)

    #########################################
    #
    # Private Methods
    #
    #########################################

    def _create_response_json_content(self, resultText) -> Dict:
        req_content = self.request['content']
        content = {'action': req_content['action'],
                   'query': req_content['query'],
                   'result': resultText}

        content_encoding = 'utf-8'
        response = {
            'content_bytes': self._json_encode(content, content_encoding),
            'content_type': 'text/json',
            'content_encoding': content_encoding,
        }
        return response

    def _create_response_binary_content(self, resultText) -> Dict:
        req_content = self.request['content']
        content = {'action': req_content['action'],
                   'query': req_content['query'],
                   'result': resultText}

        content_encoding = 'utf-8'
        content_binary = self._binary_encode(content, content_encoding)

        response = {
            "content_bytes": content_binary,
            "content_type": "binary/custom-server-binary-type",
            "content_encoding": content_encoding,
        }
        return response

    def _reset_read_state(self):
        self._jsonheader_len = None
        self.jsonheader = {}
        self.request = {}
        self._request_is_text = False
        self._sent_success = False
        self.response_created = False

    #########################################
    #
    # Public Methods
    #
    #########################################

    def read(self):
        # read sockets
        try:
            self._read()
        except ConnectionError:
            # This is thrown if the server or the client shut down. If
            # the client shuts down, the server should just keep waiting
            # for a new client to appear, so nothing happens
            pass

        self.process_read()

        # Set selector to listen for write events, we're done reading.
        self._set_selector_events_mask('w')

    def process_read(self):
        # The data is transferred with a header that starts with two bytes
        # which gives the length of the rest of the header (the header also
        # has variable length).  The last section contains the data. Each
        # of these are processed one at a time, and the buffer, which is
        # stored in self._recv_buffer, is trimmed after each state is looked
        # at so that by the end, self._recv_buffer just holds the data (action,
        # request, and response).

        if self._jsonheader_len is None:
            self.process_protoheader()

        if self._jsonheader_len is not None:
            if self.jsonheader == {}:
                self.process_jsonheader()

        if self.jsonheader != {}:
            if self.request == {}:
                self.process_request()

    def write(self):
        if self.request:
            if not self.response_created:
                self.create_response()

        self._write()

        # Close when the buffer is drained. The response has been sent.
        # Note that the Message class only handles one message per connection,
        # so after the response is written there is nothing left to do.
        # For something like the MultiVu Socket Server, in which it would be
        # normal to be querying the server multiple times, the close statement
        # probably needs to be moved.
        if self._sent_success and not self._send_buffer:
            self._check_exit()
            self._reset_read_state()
            # Set selector to listen for read events, we're done writing.
            self._set_selector_events_mask('r')

            # if there is more to read, then continue to read the buffer
            if self._recv_buffer:
                self.process_read()

    def process_request(self):
        # read the buffer into 'data'
        content_len = self.jsonheader['content-length']
        if len(self._recv_buffer) < content_len:
            return

        if self._request_is_text:
            req = self._text_decode(self._recv_buffer, 'utf-8')
            # clear the buffer
            self._recv_buffer = b''
            # parse the request
            req_list = req.split(' ')
            if len(req_list) > 0:
                action = req_list.pop(0)
                query = ', '.join(req_list)
                self.request = self.create_request(action, query)
            self._log_received_result(repr(self.request["content"]))
        else:
            data = self._recv_buffer[:content_len]
            encoding = self.jsonheader['content-encoding']

            # clear the request from the buffer
            self._recv_buffer = self._recv_buffer[content_len:]

            # process 'data'
            if self.jsonheader['content-type'] == 'text/json':
                content = self._json_decode(data, encoding)
                action = content['action']
                query = content['query']
                self.request = self.create_request(action, query)
                self._log_received_result(repr(self.request["content"]))
            else:
                # Binary or unknown content-type
                content = self._binary_decode(data, encoding)
                action = content['action']
                query = content['query']
                self.request = self.create_response(action, query)
                self._log_received_result(self.jsonheader["content-type"])

    def create_response(self):
        content = self.request['content']
        action = content['action']
        query = content['query']
        result = ''

        message = ''
        if action == 'START':
            flavor_name = self.qd_command.instrument.name
            result = f'Connected to {flavor_name} MultiVuServer at {self.addr}'
            # change the query to show if the verbose flag was selected
            self.request['content']['query'] = self._start_to_str()
        elif action == 'EXIT':
            result = 'Closing client and exiting server.'
            # Use the query to confirm the command was sent and received
            self.request['content']['query'] = action
            raise ConnectionAbortedError
        elif action == 'CLOSE':
            result = f'Client {self.addr} disconnected.'
            self.logger.info(result)
            # Use the query to confirm the command was sent and received
            self.request['content']['query'] = action
            self.connected = False
        elif action:
            command = f'{action} {query}'
            try:
                result = self.qd_command.parse_cmd(command)
            except MultiPyVuException as e:
                result = f'MultiVuError:  {e}'
        else:
            result = f"The command '{action}' has not been implemented."
        self.response = {'action': action, 'query': query, 'result': result}

        if self._request_is_text:
            message = self._text_encode(result, 'utf-8')
        else:
            if self.jsonheader['content-type'] == 'text/json':
                response = self._create_response_json_content(result)
            else:
                # Binary or unknown content-type
                response = self._create_response_binary_content(result)
            message = self._create_message(**response)
        self.response_created = True
        self._send_buffer += message

    def connect_sock(self):
        '''
        Accept a socket connection and update the selector.
        '''
        # Should be ready to read
        self.sock, self.addr = self.sock.accept()
        self.logger.info(f'Accepted connection from {self.addr}')
        self.sock.setblocking(False)
