import time
import sys
import os
import getpass
import logging
from daemon import Daemon
import configparser
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler


class LoggingEventHandler(PatternMatchingEventHandler):
    """Logs all the events captured."""

    def __init__(self):
        super(LoggingEventHandler, self).__init__(ignore_patterns=['*/_fileMonitoring.log'])
        if True:
            delattr(self, 'on_created')

    def on_moved(self, event):
        super(LoggingEventHandler, self).on_moved(event)

        what = 'directory' if event.is_directory else 'file'
        logging.info("Moved %s: from %s to %s", what, event.src_path,
                     event.dest_path)

    def on_created(self, event):
        super(LoggingEventHandler, self).on_created(event)

        what = 'directory' if event.is_directory else 'file'
        logging.info("Created %s: %s", what, event.src_path)

    def on_deleted(self, event):
        super(LoggingEventHandler, self).on_deleted(event)

        what = 'directory' if event.is_directory else 'file'
        logging.info("Deleted %s: %s", what, event.src_path)

    def on_modified(self, event):
        super(LoggingEventHandler, self).on_modified(event)

        what = 'directory' if event.is_directory else 'file'
        logging.info("Modified %s: %s", what, event.src_path)

    def on_opened(self, event):
        super(LoggingEventHandler, self).on_opened(event)

        what = 'directory' if event.is_directory else 'file'
        logging.info("Opened %s: %s", what, event.src_path)

    def on_closed(self, event):
        super(LoggingEventHandler, self).on_closed(event)

        what = 'directory' if event.is_directory else 'file'
        logging.info("Closed %s: %s", what, event.src_path)

class MyDaemon(Daemon):

    def __init__(self, pid, path):
        super().__init__(pid, stdin='/dev/stdin', stdout='/dev/stdout', stderr='/dev/stderr')
        self.path  = path

    def run(self):
        event_handler = LoggingEventHandler()    
        observer = Observer()
        observer.schedule(event_handler, self.path, recursive=True)  
        observer.start() 
        try:
            while True:
                time.sleep(0.1)
        except KeyboardInterrupt:
            observer.stop()
            observer.join()
 


if __name__ == '__main__':
    config = configparser.ConfigParser()
    if(not config.read('.fsms/watcher.ini')):
        sys.stderr.write('Error: Failed to read config file.')
        sys.exit(4)

    path = config.get('SETUP', 'watch')

    user = getpass.getuser()
    logging.basicConfig(filename='.fsms/_fileMonitoring.log', filemode='a', level=logging.INFO,
                        format=f'USER: {user}' + ' | ' + '%(asctime)s | %(process)d | %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')  


    daemon = MyDaemon('/tmp/daemon-example.pid', path)
    if len(sys.argv) == 2:
        if 'start' == sys.argv[1]:
                daemon.start()
        elif 'stop' == sys.argv[1]:
                daemon.stop()
        elif 'restart' == sys.argv[1]:
                daemon.restart()
        else:
            print("Unknown command")
            sys.exit(2)
        sys.exit(0)
    else:
        print("usage: %s start|stop|restart" % sys.argv[0])
        sys.exit(2)  

    # event_handler = LoggingEventHandler()    
    # observer = Observer()
    # observer.schedule(event_handler, path, recursive=True)  
    # observer.start() 


    # try:
    #     while True:
    #         time.sleep(0.1)
    # except KeyboardInterrupt:
    #     observer.stop()
    #     observer.join()
