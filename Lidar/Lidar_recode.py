import datetime
import json
import threading
import serial_lidar
import time
import os

LIDAR_RECORD_GAP = 0.5

class Lidar_recoder:
    def __init__(self, save_directory) -> None:
        self.lidar = serial_lidar.LidarModule()
        self.data = {}
        self.record_gap = LIDAR_RECORD_GAP
        self.last_record_time = datetime.datetime.now().timestamp()
        self.save_directory = save_directory

        self.recoder_thread = threading.Thread(target=self._record_lidar)
        self.keep_recording = True

    def init_data(self):
        self.data = {}

    def getTimestamp(self):
        return datetime.datetime.now().timestamp()
    
    def _record_lidar(self):
        while self.keep_recording:
            timestamp = int(self.getTimestamp())
            self.data[timestamp] = self.lidar.getRange()

    def checkConnection(self):
        return self.lidar.checkConnection()

    def start(self):
        self.start_timestamp = str(self.getTimestamp())
        self.keep_recording = True
        self.recoder_thread.start()

    def stop(self):
        self.keep_recording = False
        save_file_directory = os.path.join(self.save_directory, f'lidar_record_{self.start_timestamp}.json' )
        self.recoder_thread.join()

        with open(save_file_directory, 'w') as f:
            json.dump(self.data, f, indent=4)

        self.init_data()

        print('saved')
        

if __name__ == '__main__':
    lidar = Lidar_recoder('/home/nvidia/recorded/')
    lidar.start()
    time.sleep(3)
    lidar.stop()
    