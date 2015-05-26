import socket, threading, time,sys

sockets = {}

class cliente(threading.Thread):

    def __init__(self,sc,nombre):
        threading.Thread.__init__(self)
        self.fich = open('C:\Users\Equipo101\Desktop\\2015pro\Serviciowindowsservidorchat\clienlog.txt','a')
        self.nombre = nombre
        self.sc = sc

    def run(self):
        global sockets
        self.broadcast('Conectado '+self.nombre)
        while True:
            try:
                received = self.sc.recv(1024)
                a = received.decode('utf-8')
                self.log(self.nombre+': '+str(a)+'\n')
                self.broadcast(self.nombre+': '+str(a))
            except Exception,e:
                self.fich.write('Excepcion:\n')
                self.fich.write(str(e))
                self.fich.write('Fin Excepcion\n')
                self.fich.flush()
                break
        del sockets[str(self.nombre)]
        self.broadcast('Desconectado '+self.nombre)

    def broadcast(self,msg):
        global sockets
        try:
            for usu,sock in sockets.items():
                sock.send(msg)
        except Exception,ex:
            self.fich.write(str(ex))
            self.fich.flush()

    def log(self,msg):
        self.fich.write(str(msg))
        self.fich.flush()

class server(threading.Thread):

    def __init__(self):
        self.fich = open('C:\Users\Equipo101\Desktop\\2015pro\Serviciowindowsservidorchat\log.txt','a')
        threading.Thread.__init__(self)

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
                sockets[str(nombre)] = sc
                t = cliente(sc,str(nombre))
                t.setDaemon = True
                t.start()
            except Exception,e:
                self.fich.write(str(e))
                self.fich.flush()





