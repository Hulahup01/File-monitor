import logging
from watchdog.events import PatternMatchingEventHandler


class LoggingEventHandler(PatternMatchingEventHandler):
    """Logs all the events captured."""

    def __init__(self, ignore_pattern=[], **kwargs):
        super(LoggingEventHandler, self).__init__(ignore_patterns=ignore_pattern)
        all = kwargs.get('all', False)
        self.on_moved_opt = kwargs.get('move', False ^ all)
        self.on_created_opt = kwargs.get('create', False ^ all)
        self.on_deleted_opt = kwargs.get('delete', False ^ all)
        self.on_modified_opt = kwargs.get('modify', False ^ all)
        self.on_opened_opt = kwargs.get('open', False ^ all)
        self.on_closed_opt = kwargs.get('close', False ^ all)

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
        if self.on_opened_opt:
            super(LoggingEventHandler, self).on_opened(event)

            what = 'directory' if event.is_directory else 'file'
            logging.info("Opened %s: %s", what, event.src_path)

    def on_closed(self, event):
        if self.on_closed_opt:
            super(LoggingEventHandler, self).on_closed(event)

            what = 'directory' if event.is_directory else 'file'
            logging.info("Closed %s: %s", what, event.src_path)