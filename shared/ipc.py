import zmq

CTX = zmq.Context.instance()


def server(bind_addr):
    sock = CTX.socket(zmq.REP)
    sock.bind(bind_addr)
    return sock


def client(connect_addr):
    sock = CTX.socket(zmq.REQ)
    sock.connect(connect_addr)
    return sock
