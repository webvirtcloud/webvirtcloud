#!/usr/bin/env python3

import libvirt
import logging
from http import cookies
from xml.etree import ElementTree
from optparse import OptionParser
from websockify import WebSocketProxy
from websockify import ProxyRequestHandler


def get_xml_data(xml, path=None, element=None):
    res = ""
    if not path and not element:
        return ""

    tree = ElementTree.fromstring(xml)
    if path:
        child = tree.find(path)
        if child is not None:
            if element:
                res = child.get(element)
            else:
                res = child.text
    else:
        res = tree.get(element)
    return res


parser = OptionParser()
parser.add_option("-v", "--verbose", dest="verbose", action="store_true", help="Verbose mode", default=False)

parser.add_option("-d", "--debug", dest="debug", action="store_true", help="Debug mode", default=False)

parser.add_option("-H", "--host", dest="host", action="store", help="Listen host", default="0.0.0.0")

parser.add_option("-p", "--port", dest="port", action="store", help="Listen port", default=6080)

parser.add_option("-c", "--cert", dest="cert", action="store", help="Certificate file path", default="cert.pem")

(options, args) = parser.parse_args()

FORMAT = "%(asctime)s - %(name)s - %(levelname)s : %(message)s"
if options.debug:
    logging.basicConfig(level=logging.DEBUG, format=FORMAT)
    options.verbose = True
elif options.verbose:
    logging.basicConfig(level=logging.INFO, format=FORMAT)
else:
    logging.basicConfig(level=logging.WARNING, format=FORMAT)


def get_conn_data(token):
    port = None
    try:
        conn = libvirt.open("qemu:///system")
        for dom in conn.listDomainsID():
            if token == dom.UUIDString():
                xml = dom.XMLDesc()
                console_type = get_xml_data(xml, "devices/graphics", "type")
                port = get_xml_data(xml, f"devices/graphics[@type='{console_type}']", "port")
        conn.close()
    except libvirt.libvirtError as err:
        logging.error(f"Fail to retrieve console connection infos for token {token} : {err}")
        raise
    return port


class CompatibilityMixIn(object):
    def _new_client(self, daemon, socket_factory):
        cookie = cookies.SimpleCookie()
        cookie.load(self.headers.get("cookie"))

        if "token" not in cookie:
            logging.error("- Token not found")
            return False

        console_host = "localhost"
        console_port = get_conn_data(cookie.get("token").value)

        cnx_debug_msg = "Connection Info:\n"
        cnx_debug_msg += f"       - VNC host: {console_host}\n"
        cnx_debug_msg += f"       - VNC port: {console_port}"
        logging.debug(cnx_debug_msg)

        # Direct access
        tsock = socket_factory(console_host, console_port, connect=True)

        if self.verbose and not daemon:
            print(self.traffic_legend)

        # Start proxying
        try:
            self.vmsg(f"{console_host}:{console_port}: Websocket client or Target closed")
            self.do_proxy(tsock)
        except Exception:
            raise


class NovaProxyRequestHandler(ProxyRequestHandler, CompatibilityMixIn):
    def msg(self, *args, **kwargs):
        self.log_message(*args, **kwargs)

    def vmsg(self, *args, **kwargs):
        if self.verbose:
            self.msg(*args, **kwargs)

    def new_websocket_client(self):
        """
        Called after a new WebSocket connection has been established.
        """
        # Setup variable for compatibility
        daemon = self.server.daemon
        socket_factory = self.server.socket

        self._new_client(daemon, socket_factory)


if __name__ == "__main__":
    # Create the WebSocketProxy with NovaProxyRequestHandler handler
    server = WebSocketProxy(
        RequestHandlerClass=NovaProxyRequestHandler,
        listen_host=options.host,
        listen_port=options.port,
        source_is_ipv6=False,
        verbose=options.verbose,
        cert=options.cert,
        key=None,
        ssl_only=False,
        daemon=False,
        record=False,
        web=False,
        traffic=False,
        target_host="ignore",
        target_port="ignore",
        wrap_mode="exit",
        wrap_cmd=None,
    )
    server.start_server()
