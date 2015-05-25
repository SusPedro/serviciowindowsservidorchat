import socket, threading, time,sys

sockets = {}

class cliente(threading.Thread):
    def __init__(self,sc,clave):
        threading.Thread.__init__(self)
        self.fich = open('C:\Users\jesus\Desktop\Compartida\guiserverroomo\service\\service\clienlog.txt','a')
        self.socketslist()
        self.clave = clave
        self.sc = sc
        self.usu = 'usuariocon'

    def run(self):
        self.broadcast('Conectado '+self.usu)
        while True:
            try:
                received = self.sc.recv(1024)
                a = received.decode('utf-8')
                print("Msg:"+str(a))
                self.broadcast(self.usu+str(a))
            except Exception,e:
                self.fich.write(str(e))
                self.fich.flush()
                break
        del sockets[str(self.clave)]
        self.broadcast('Desconectado '+self.usu)

    def broadcast(self,msg):
        try:
            for usu,sock in sockets.items():
                sock.send(self.usu+': '+msg)
        except Exception,ex:
            self.fich.write(str(ex))
            self.fich.flush()

    def nameforclave(self):
        for usu,sock in sockets.items():
            if a == self.clave:
                pass

    def socketslist(self):
        self.fich.write('Lista de sockets\n')
        for i,v in sockets.items():
            self.fich.write('socket: '+str(v)+' \nclave: '+str(i))
            self.fich.write('\n')
            self.fich.flush()

class server(threading.Thread):
    def __init__(self):
        self.fich = open('C:\Users\jesus\Desktop\Compartida\guiserverroomo\service\\service\log.txt','a')
        threading.Thread.__init__(self)
        self.clave = 0

    def run(self):
        while True:
            try:
                s = socket.socket()
                s.bind(('', 44000))
                s.listen(5)
                sc, addr = s.accept()
                sockets[str(self.clave)] = sc
                t = cliente(sc,str(self.clave))
                t.setDaemon = True
                t.start()
                self.clave = self.clave +1
            except Exception,e:
                self.fich.write(str(e))
                self.fich.flush()





