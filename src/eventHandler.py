import logging
from watchdog.events import PatternMatchingEventHandler


class LoggingEventHandler(PatternMatchingEventHandler):
    """Logs all the events captured."""

    def __init__(self, ignore_pattern=[],
                 on_moved=True,on_created=True,on_deleted=True,
                 on_modified=True, on_opened=True, on_closed=True):
        super(LoggingEventHandler, self).__init__(ignore_patterns=ignore_pattern)
        self.on_moved_opt = on_moved
        self.on_created_opt = on_created
        self.on_deleted_opt = on_deleted
        self.on_modified_opt = on_modified
        self.on_opened_opt = on_opened
        self.on_closed_opt = on_closed

    def on_moved(self, event):
        if self.on_moved_opt:
            super(LoggingEventHandler, self).on_moved(event)

            what = 'directory' if event.is_directory else 'file'
            logging.info("Moved %s: from %s to %s", what, event.src_path,
                        event.dest_path)

    def on_created(self, event):
        if self.on_created_opt:
            super(LoggingEventHandler, self).on_created(event)

            what = 'directory' if event.is_directory else 'file'
            logging.info("Created %s: %s", what, event.src_path)

    def on_deleted(self, event):
        if self.on_deleted_opt:
            super(LoggingEventHandler, self).on_deleted(event)

            what = 'directory' if event.is_directory else 'file'
            logging.info("Deleted %s: %s", what, event.src_path)

    def on_modified(self, event):
        if self.on_modified_opt:
            super(LoggingEventHandler, self).on_modified(event)
    
            what = 'directory' if event.is_directory else 'file'
            if what == 'file':
                logging.info("Modified %s: %s", what, event.src_path)

    def on_opened(self, event):
        if self.on_opened:
            super(LoggingEventHandler, self).on_opened(event)

            what = 'directory' if event.is_directory else 'file'
            logging.info("Opened %s: %s", what, event.src_path)

    def on_closed(self, event):
        if self.on_closed_opt:
            super(LoggingEventHandler, self).on_closed(event)

            what = 'directory' if event.is_directory else 'file'
            logging.info("Closed %s: %s", what, event.src_path)