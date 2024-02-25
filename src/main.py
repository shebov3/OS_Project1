import win32serviceutil
import win32service
import win32event
import servicemanager
import socket
import sys
import time
import psutil
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

class PCWorkloadService(win32serviceutil.ServiceFramework):
    _svc_name_ = 'PCWorkloadService'
    _svc_display_name_ = 'PC Workload Service'

    def __init__(self, args):
        win32serviceutil.ServiceFramework.__init__(self, args)
        self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)
        socket.setdefaulttimeout(60)
        self.is_alive = True

    def SvcStop(self):
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        win32event.SetEvent(self.hWaitStop)
        self.is_alive = False

    def SvcDoRun(self):
        servicemanager.LogMsg(servicemanager.EVENTLOG_INFORMATION_TYPE,
                              servicemanager.PYS_SERVICE_STARTED,
                              (self._svc_name_, ''))
        self.main()

    def main(self):
        while self.is_alive:
            cpu_percent = psutil.cpu_percent(interval=1)
            memory_percent = psutil.virtual_memory().percent
            disk_percent = psutil.disk_usage('/').percent
            network_counters = psutil.net_io_counters()
            network_usage = f"Sent: {network_counters.bytes_sent} bytes, Received: {network_counters.bytes_recv} bytes"

            with open('workload_data.txt', 'a') as file:
                file.write(f"CPU: {cpu_percent}%\nMemory: {memory_percent}%\nDisk: {disk_percent}%\nNetwork: {network_usage}\n")
            
            if time.localtime().tm_hour % 12 == 0:
                self.send_email('shehabtarik425@yahoo.com', 'THE PASSWORD', 'doxife8116@ricorit.com', 'PC Workload Data', 'See attached', 'workload_data.txt')
            
            time.sleep(5000)

    def send_email(self, sender_email, sender_password, recipient_email, subject, body, attachment_path):
        msg = MIMEMultipart()
        msg.attach(MIMEText(body, 'plain'))

        with open(attachment_path, 'rb') as attachment:
            attachment_data = MIMEText(attachment.read(), 'base64')
            attachment_data.add_header('Content-Disposition', f'attachment; filename={attachment_path}')
            msg.attach(attachment_data)

        msg['Subject'] = subject
        msg['From'] = sender_email
        msg['To'] = recipient_email

        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, recipient_email, msg.as_string())

if __name__ == '__main__':
    if len(sys.argv) == 1:
        servicemanager.Initialize()
        servicemanager.PrepareToHostSingle(PCWorkloadService)
        servicemanager.StartServiceCtrlDispatcher()
    else:
        win32serviceutil.HandleCommandLine(PCWorkloadService)
