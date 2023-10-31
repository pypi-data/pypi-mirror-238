#!/usr/bin/env python3

"""MXHAS CLI."""
import sys
import json
import cmd2
from xhac.client import HomeClient, HACException


class MxhasCli(cmd2.Cmd):
    """MXHAS CLI."""

    intro = "Welcome to the MXHAS shell.\nType help or ? to list commands.\n"
    prompt = "> "

    connect_parser = cmd2.Cmd2ArgumentParser()
    connect_parser.add_argument("addr", help="IPv4 address")
    connect_parser.add_argument("port", help="Server Port")
    connect_parser.add_argument("mac", help="MAC address")
    connect_parser.add_argument("password", help="Login Password")

    @cmd2.with_argparser(connect_parser)
    def do_connect(self, args):
        """Connect to a HAS."""
        self.client = HomeClient(args.addr, int(args.port), args.mac, args.password)
        try:
            self.client.connect()
        except HACException:
            self.poutput("failed to connect")
            return
        self.poutput("connected")
        self.client.on_disconnect = lambda client: self.poutput("disconnected")
        self.client.on_event = lambda client, event: self.poutput(json.dumps(event))

    def do_disconnect(self, args):
        """Disconnect from a HAS."""
        self.client.disconnect()
        self.poutput("Disconnected from HAS")

    get_parser = cmd2.Cmd2ArgumentParser()
    get_parser.add_argument("path", help="Get path")
    get_parser.add_argument("params", nargs="*", help="Get paramenters")

    @cmd2.with_argparser(get_parser)
    def do_get(self, args):
        """HAS get method."""
        params = {}
        for arg in args.params:
            key, value = arg.split("=")
            params[key] = value
        status, content = self.client._get(args.path, params)
        self.poutput(f"Status: {status}")
        if content:
            self.poutput(f"Content: {content}")

    put_parser = cmd2.Cmd2ArgumentParser()
    put_parser.add_argument("path", help="Put path")
    put_parser.add_argument("content", help="Put content")

    @cmd2.with_argparser(put_parser)
    def do_put(self, args):
        """HAS put method."""
        status, content = self.client._put(args.path, args.content)
        self.poutput(f"Status: {status}")
        if content:
            self.poutput(f"Content: {content}")


def main():
    c = MxhasCli()
    sys.exit(c.cmdloop())


if __name__ == "__main__":
    main()
