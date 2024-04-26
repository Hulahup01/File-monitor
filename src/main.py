import time
import sys
import getpass
import logging
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler


class LoggingEventHandler(PatternMatchingEventHandler):
    """Logs all the events captured."""

    def __init__(self):
        super(LoggingEventHandler, self).__init__(ignore_patterns=['*/_fileMonitoring.log'])

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


if __name__ == '__main__':
    path = sys.argv[1] if len(sys.argv) > 1 else None
    if path is None:
        raise ValueError('Error: Path argument is missing.')
    user = getpass.getuser()
    logging.basicConfig(filename='_fileMonitoring.log', filemode='a', level=logging.INFO,
                        format=f'USER: {user}' + ' | ' + '%(asctime)s | %(process)d | %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')    

    event_handler = LoggingEventHandler()    
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)  
    observer.start() 

    try:
        while True:
            time.sleep(0.1)
    except KeyboardInterrupt:
        observer.stop()
        observer.join()
