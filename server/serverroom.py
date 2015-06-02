import socket, threading,sys,os,time
import servicemanager

sockets = {}


class cliente(threading.Thread):

    def __init__(self,sc,nombre,lock):
        threading.Thread.__init__(self)
        sys.stderr = file(os.path.join(os.path.dirname(__file__), 'log', 'log.log'),'a')
        self.nombre = nombre
        self.sc = sc
        self.lock = lock

    def run(self):
        global sockets
        self.broadcast(time.strftime("%I:%M:%S")+' se ha conectado '+self.nombre)
        self.log(time.strftime("%I:%M:%S")+' se ha conectado '+self.nombre)
        while True:
            try:
                received = self.sc.recv(1024)
                a = received.decode('utf-8')
                with self.lock:
                    self.broadcast(self.nombre+': '+str(a))
                self.log(time.strftime("%I:%M:%S")+' | '+self.nombre+' | '+str(a))
            except Exception,e:
                sys.stderr.write(str(e)+"\n")
                break
        with self.lock:
            del sockets[str(self.nombre)]
        self.broadcast(time.strftime("%I:%M:%S")+' se ha desconectado '+self.nombre)
        self.log(time.strftime("%I:%M:%S")+' se ha desconectado '+self.nombre)

    def broadcast(self,msg):
        global sockets
        try:
            for usu,sock in sockets.items():
                sock.send(msg)
        except Exception,e:
            sys.stderr.write(str(e)+"\n")
            pass

    def log(self,msg):
        sys.stderr.write(str(msg)+"\n")


class server(threading.Thread):

    def __init__(self,lock):
        threading.Thread.__init__(self)
        sys.stderr = file(os.path.join(os.path.dirname(__file__), 'log', 'log.log'),'a')
        sys.stderr.write('\nServicio iniciado '+time.strftime("%d/%m/%Y")+' a las '+time.strftime("%I:%M:%S")+'\n')
        self.lock = lock

    def run(self):
        global sockets
        while True:
            try:
                s = socket.socket()
                s.bind(('', 44000))
                s.listen(5)
                sc, addr = s.accept()
                """obtener el nombre"""
                recibido = sc.recv(1024)
                deco = recibido.decode('utf-8')
                nombre = str(deco)
                """"""
                with self.lock:
                    sockets[str(nombre)] = sc
                t = cliente(sc,str(nombre),self.lock)
                t.setDaemon = True
                t.start()
                """servicemanager log"""
                servicemanager.LogMsg(
                    servicemanager.EVENTLOG_INFORMATION_TYPE,
                    0xF000, # Generic message
                    ('conectado cliente', ''))
            except Exception,e:
                sys.stderr.write(str(e)+"\n")

    def log(self,msg):
        sys.stderr.write(str(msg)+"\n")




