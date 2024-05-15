import os
import sys
import time
import getpass
import logging
import configparser
from daemon import Daemon
from watchdog.observers import Observer
from eventHandler import LoggingEventHandler


class FSMSDaemon(Daemon):

    def __init__(self, pidfile, main_path):
        super().__init__(pidfile, stdin='/dev/stdin', stdout='/dev/stdout', stderr='/dev/stderr')
        self.main_path = main_path
        self.fsms_path = main_path + '/.fsms'
        self.config_path = self.fsms_path + '/watcher.ini'
        self.log_path = self.fsms_path + '/_fileMonitoring.log'
        self.config = configparser.ConfigParser()
        self.events = {}
        self.exclude = []
        self.recursive = True

    def run(self):
       
        if not self.config.read(self.config_path):
            sys.stderr.write('Error: Failed to read config file.\n')
            sys.exit(1)

        if self.config.get('SETUP','watch') != self.main_path:
            sys.stderr.write('Error: The paths in .ini and the call path are different\n')
            sys.exit(1)

        try:
            self.events = self.config.get('SETUP', 'events').strip().split(',')
            self.events = {event.strip(): True for event in self.events}
        except:
            sys.stderr.write('Error: incorrect option "events"\n')
            sys.exit(1)

        try:
            self.exclude = self.config.get('SETUP', 'excluded').strip().split(',')
            self.exclude = [el.strip() for el in self.exclude]
        except:
            sys.stderr.write('Error: incorrect option "excluded"\n')
            sys.exit(1)

        try:
            self.recursive = self.config.getboolean('SETUP', 'recursive')
        except:
            sys.stderr.write('Error: incorrect option "recursive"\n')
            sys.exit(1)

        user = getpass.getuser()
        logging.basicConfig(filename=self.log_path, filemode='a', level=logging.INFO,
                            format=f'USER: {user}' + ' | ' + '%(asctime)s | %(process)d | %(message)s',
                            datefmt='%Y-%m-%d %H:%M:%S')

        event_handler = LoggingEventHandler(ignore_pattern=['*/.fsms/*'] + self.exclude, **self.events)    
        observer = Observer()
        observer.schedule(event_handler, self.main_path, recursive=self.recursive)  
        observer.start()
        
        while observer.is_alive():
            time.sleep(1)
            if not os.path.exists(self.fsms_path) or not os.path.exists(self.log_path):
                observer.stop()
                self.stop()
                exit(1)