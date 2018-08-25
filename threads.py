import threading


class ServerThread(threading.Thread):
    def __init__(self,server):
        threading.Thread.__init__(self)
        self.server = server