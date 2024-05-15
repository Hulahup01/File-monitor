import time
import sys
import getpass
import logging
import os
import hashlib
import subprocess
import configparser
from watchdog.observers import Observer
from daemon import Daemon
from eventHandler import LoggingEventHandler


class FSMSDaemon(Daemon):

    def __init__(self, pidfile, main_path):
        super().__init__(pidfile, stdin='/dev/stdin', stdout='/dev/stdout', stderr='/dev/stderr')
        self.main_path = main_path
        self.fsms_path = main_path + '/.fsms'
        self.config_path = self.fsms_path + '/watcher.ini'
        self.log_path = self.fsms_path + '/_fileMonitoring.log'
        self.config = configparser.ConfigParser()

    def run(self):
       
        if(not self.config.read(self.config_path)):
            sys.stderr.write('Error: Failed to read config file.')
            sys.exit(4)

        user = getpass.getuser()
        logging.basicConfig(filename=self.log_path, filemode='a', level=logging.INFO,
                            format=f'USER: {user}' + ' | ' + '%(asctime)s | %(process)d | %(message)s',
                            datefmt='%Y-%m-%d %H:%M:%S')

        event_handler = LoggingEventHandler(ignore_pattern=['*/.fsms/*'])    
        observer = Observer()
        observer.schedule(event_handler, self.main_path, recursive=True)  
        observer.start()
        
        while observer.is_alive():
            time.sleep(1)
            if not os.path.exists(self.fsms_path):
                observer.stop()
                self.stop()
                exit(0)
 


if __name__ == '__main__':
    main_path = sys.argv[1] if len(sys.argv) > 1 else None
    if main_path is None:
        raise ValueError('Error: Path argument is missing.')

    pidfile_path = f'/tmp/deamon_pid_{hashlib.sha256(main_path.encode()).hexdigest()}.pid'

    daemon = FSMSDaemon(pidfile_path, main_path)

    if len(sys.argv) == 3:
        if 'start' == sys.argv[2]:
            daemon.start()
        elif 'stop' == sys.argv[2]:
            daemon.stop()
        elif 'restart' == sys.argv[2]:
            daemon.restart()
        elif 'status' == sys.argv[2]:
            daemon.status()
        elif 'debug' == sys.argv[2]: # option for debugging
            daemon.run()
        else:
            print("Unknown command")
            sys.exit(2)
        sys.exit(0)
    else:
        print("Uage: %s path start|stop|restart|status|debug" % sys.argv[0])
        sys.exit(2)  