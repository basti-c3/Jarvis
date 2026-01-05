import zmq

CTX = zmq.Context.instance()


def server(bind_addr, stream_pattern=zmq.REP):
    sock = CTX.socket(stream_pattern)
    sock.bind(bind_addr)
    return sock


def client(connect_addr, stream_pattern=zmq.REQ):
    sock = CTX.socket(stream_pattern)
    sock.connect(connect_addr)
    return sock
