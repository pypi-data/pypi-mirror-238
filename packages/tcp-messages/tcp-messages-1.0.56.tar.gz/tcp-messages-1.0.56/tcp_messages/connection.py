from .message_list import MessageList
from .message import Message, MessageParts, MessagePart
import socket


class Connection:

    class State:
        Open = 1
        Close = 4

    def __init__(self, s: socket.socket, failed_message=None):
        self.socket = s
        self.socket.settimeout(0.001)
        self.failed_message = failed_message
        self.pending_messages = MessageList()
        self.state = None
        self.partials = dict()
        self.peek()

    def close(self):
        self.socket.close()
        self.state = Connection.State.Close

    def send(self, message: Message) -> bool:
        message_parts = MessageParts(message)
        for part in message_parts:
            message_str = str(part)
            message_bytes = message_str.encode()
            message_bytes += b'\x00'
            if self.socket.send(message_bytes) != len(message_bytes):
                return False
        return True

    def peek(self):
        try:
            data = self.socket.recv(1, socket.MSG_PEEK)
        except socket.timeout:
            self.state = Connection.State.Open
            return False
        except:
            self.state = Connection.State.Close
            return False
        if len(data) == 0:
            self.state = Connection.State.Close
            return False
        else:
            self.state = Connection.State.Open
            return True

    def receive(self):
        if not self.state == Connection.State.Open: #if the connection is not open
            return
        if self.pending_messages:
            return self.pending_messages.dequeue() #if there are pending messages retrun the oldest
        if not self.peek():
            return None #if there are no messages
        data = bytes()
        try:
            data = self.socket.recv(8192)
        except socket.timeout as e:
            pass
        except Exception as e:
            self.state = Connection.State.Close #if connection was closed from the other side
        else:
            if data:
                messages_str = data.decode().split('\x00')
                for message_str in messages_str:
                    if message_str:
                        try:
                            message_part = MessagePart.parse(message_str) # creates a new message instance
                            if message_part.parts <= 1:
                                self.pending_messages.queue(message_part.to_message())
                            else:
                                if message_part.id not in self.partials:
                                    self.partials[message_part.id] = MessageParts()
                                self.partials[message_part.id].append(message_part)
                                if self.partials[message_part.id].is_ready():
                                    self.pending_messages.queue(self.partials[message_part.id].join())
                                    del self.partials[message_part.id]
                        except:
                            if self.failed_message:
                                self.failed_message(message_str)
        return self.pending_messages.dequeue()

    def __bool__(self):
        self.peek()
        return self.state == Connection.State.Open
