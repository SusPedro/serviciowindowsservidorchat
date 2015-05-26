import win32serviceutil
import win32service
import win32event
from server import serverroom
import threading

class JesusService(win32serviceutil.ServiceFramework):
    _svc_name_ = "JesusService2"
    _svc_display_name_ = "AaJesusService2"
    _svc_description_ = "Proyecto Jesus2"

    def __init__(self, args):
        win32serviceutil.ServiceFramework.__init__(self, args)
        # Evento que se usara para detener el servicio
        self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)

    def SvcStop(self):
        # Se informa al SMC que se esta deteniendo el servicio
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        # Establece el evento de parada
        win32event.SetEvent(self.hWaitStop)

    def SvcDoRun(self):
        lock = threading.Lock()
        s = serverroom.server(lock)
        s.setDaemon = True
        s.start()
        # El servicio no hace nada, simplemente esperar al evento de detencion
        win32event.WaitForSingleObject(self.hWaitStop, win32event.INFINITE)

if __name__=='__main__':
    win32serviceutil.HandleCommandLine(JesusService)

