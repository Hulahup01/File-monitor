import sys
import hashlib
from fsmsDaemon import FSMSDaemon


def main():
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
        print('Uage: %s path start|stop|restart|status|debug' % sys.argv[0])
        sys.exit(2)  


if __name__ == '__main__':
    main()