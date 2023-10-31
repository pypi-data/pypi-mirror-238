from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import sys
import os
import subprocess
import time

base_path = os.path.dirname(os.path.abspath(__file__))
venv_python_path = os.path.join(base_path, '../venv', 'Scripts', 'python.exe')


class Watcher(FileSystemEventHandler):
    def __init__(self, process):
        self.process = process

    def on_modified(self, event):
        if event.src_path.endswith('.peeey'):
            print('Files changed, restarting in 10 seconds')
            time.sleep(10)
            if self.process:
                subprocess.run(["taskkill", "/F", "/PID", str(self.process.pid)])
            self.process = subprocess.Popen([venv_python_path, "main.py"], stdout=sys.stdout, stderr=sys.stderr)

    def restart_process(self):
        self.process = subprocess.Popen([venv_python_path, "main.py"], stdout=sys.stdout, stderr=sys.stderr)


if __name__ == '__main__':
    process = subprocess.Popen([venv_python_path, "main.py"], stdout=sys.stdout, stderr=sys.stderr)
    observer = Observer()
    event_handler = Watcher(process)
    observer.schedule(event_handler, path='..', recursive=True)
    observer.start()

    try:
        while True:
            time.sleep(1)
            if event_handler.process.poll() is not None:
                print('Process has terminated. Restarting...')
                event_handler.restart_process()
    except KeyboardInterrupt:
        observer.stop()
        observer.join()
