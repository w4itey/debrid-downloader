
# import time module, Observer, FileSystemEventHandler
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from database.db import db, ingest # type: ignore
from Service.realdebrid import get_torrent_hash  # type: ignore
 
class OnMyWatch:
    # Set the directory on watch
 
    def __init__(self, folder):
        self.observer = Observer()
        self.watchDirectory = folder
 
    def run(self):
        event_handler = Handler()
        self.observer.schedule(event_handler, self.watchDirectory, recursive = False)
        self.observer.start()
        try:
            while True:
                time.sleep(5)
        except:
            self.observer.stop()
            print("Observer Stopped")
 
        self.observer.join()
 
 
class Handler(FileSystemEventHandler):
 
    @staticmethod
    def on_any_event(event):
        if event.is_directory:
            return None
 
        elif event.event_type == 'created':
            # Event is created, you can process it now
            print("Watchdog received created event - % s." % event.src_path)
            db.init(ingest)
            torrent = get_torrent_hash(event.src_path)
            entry = db(hash = torrent['hash'])

        elif event.event_type == 'modified':
            # Event is modified, you can process it now
            print("Watchdog received modified event - % s." % event.src_path)
             
 
if __name__ == '__main__':
    watch = OnMyWatch()
    watch.run()
