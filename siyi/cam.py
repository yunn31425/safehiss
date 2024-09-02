import socketio
import base64
import gi
import subprocess
import multiprocessing
import time
import os
import sys

import threading

gi.require_version('Gst', '1.0')
gi.require_version('GstApp', '1.0')
from gi.repository import Gst, GLib, GstApp

SERVER_URL = 'http://203.255.57.124:5000'
RTSP_URL = "rtsp://192.168.144.25:8554/video1"
RTSP_IP = "192.168.144.25"

EO = 1
THERAML = 2

class camClient:
    '''
    서버에 접속 및 영상 데이터 전송, 명령 수신 등의 동작 총괄

    1. 서버에 접속 및 상태 전송
    2. 서버가 보내는 명령 수신 및 동작
    3. 명령 : 영상 녹화, 
    '''
    def __init__(self, server_url, rtsp_url, rtsp_ip) -> None:
        self.sio = socketio.Client()
        self.server_url = server_url
        self.rtsp_url = rtsp_url
        self.rtsp_ip = rtsp_ip
        self.pipeline = None

        self.sio.on('connect', self.on_connect)
        self.sio.on('disconnect', self.on_disconnect)
        self.sio.on('message', self.message_handler)
        self.sio.on('response', self.on_response)

    def on_connect(self):
        self.checkCam()
        self.sio.send('start')
        self.start_gstreamer()

    def on_disconnect(self):
        self.sio.send('stop')
        self.stop_gstreamer()
    
    def message_handler(self):
        pass

    def connectServer(self):
        self.sio.connect(self.server_url)
        self.sio.wait()
    
    def on_response(self, data):
        print(f'Server response: {data}')

    def on_new_sample(self, sink):
        sample = sink.emit("pull-sample")
        buf = sample.get_buffer()
        
        success, map_info = buf.map(Gst.MapFlags.READ)
        if success:
            frame_data = map_info.data
            # JPEG 인코딩된 데이터를 Base64로 인코딩
            jpg_as_text = base64.b64encode(frame_data).decode('utf-8')
            # 서버로 프레임 전송
            self.sio.emit('video_frame', jpg_as_text)
            # print(1)
            print(jpg_as_text)
            buf.unmap(map_info)
        return Gst.FlowReturn.OK

    def start_gstreamer(self):
        # GStreamer 파이프라인 생성
        self.pipeline = Gst.parse_launch(
            f'rtspsrc location={self.rtsp_url} latency=200 ! rtph265depay ! h265parse ! avdec_h265 ! videoconvert ! jpegenc ! appsink name=sink'
        )
        
        # appsink 요소 가져오기
        sink = self.pipeline.get_by_name('sink')
        # emit-signals 속성을 True로 설정
        sink.set_property('emit-signals', True)
        # 신호 연결
        sink.connect("new-sample", self.on_new_sample)

        # 파이프라인 실행
        self.pipeline.set_state(Gst.State.PLAYING)

        # GLib MainLoop 실행 (파이프라인이 멈출 때까지 계속 실행)
        self.loop = GLib.MainLoop()
        try:
            self.loop.run()
        except KeyboardInterrupt:
            pass
        finally:
            self.pipeline.set_state(Gst.State.NULL)

    def stop_gstreamer(self):
        if self.pipeline:
            self.pipeline.set_state(Gst.State.NULL)
            self.loop.quit()

    def checkCam(self, timeout=3):
        try:
            # ping 명령어 실행, 타임아웃 3초 설정
            subprocess.run(
                ["ping", "-c", "1", "-W", str(timeout), self.rtsp_ip],
                check=True,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
            # print(f"Host {self.rtsp_ip} is reachable.")
            return True
        except subprocess.CalledProcessError:
            print(f"Host {self.rtsp_ip} is not reachable. RESET")

            ip_add_order = ["sudo", "ip", "addr", "add", "192.168.144.30/24", "dev", "eth0"]
            interface_order = ["sudo", "ethtool", "-s", "eth0", "speed", "10", "duplex", "full"]

            result_ip_add =  subprocess.run(ip_add_order, stdout=subprocess.PIPE)
            result_interface = subprocess.run(interface_order, stdout=subprocess.PIPE)

            if result_interface and result_ip_add:
                return True
            
            else:
                return False

class RTSPRecord:
    def __init__(self, video_num, rtsp_ip)  -> None:
        self._video_num = video_num
        self._file_name = ""
        self._rtsp_ip = rtsp_ip

        # 파일 이름 생성
        timestamp = int(time.time())
        video_type = "EO" if video_num == 1 else "Thermal"
        self._file_name = f"recorded/{video_type}_{timestamp}.mp4"

        # GStreamer 파이프라인 문자열
        self.pipeline_str_record = (
            f"rtspsrc location=rtsp://192.168.144.25:8554/video{video_num} latency=100 ! "
            "rtph265depay ! h265parse ! avdec_h265 ! videoconvert ! "
            f"x264enc ! mp4mux ! filesink location={self._file_name}"
        )

        self.pipeline = None
        self.loop = None
        self.stop_event = multiprocessing.Event()

        Gst.init(None)


    def checkCam(self, timeout=3):
        try:
            # ping 명령어 실행, 타임아웃 3초 설정
            subprocess.run(
                ["ping", "-c", "1", "-W", str(timeout), self._rtsp_ip],
                check=True,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
            # print(f"Host {self.rtsp_ip} is reachable.")
            return True
        except subprocess.CalledProcessError:
            print(f"Host {self._rtsp_ip} is not reachable. RESET")

            ip_add_order = ["sudo", "ip", "addr", "add", "192.168.144.30/24", "dev", "eth0"]
            interface_order = ["sudo", "ethtool", "-s", "eth0", "speed", "10", "duplex", "full"]

            result_ip_add =  subprocess.run(ip_add_order, stdout=subprocess.PIPE)
            result_interface = subprocess.run(interface_order, stdout=subprocess.PIPE)

            if result_interface and result_ip_add:
                return True
            
            else:
                return False
            
    def _gstreamer_pipeline(self):
        # 파이프라인 생성
        print(self.pipeline_str_record)
        self.pipeline = Gst.parse_launch(self.pipeline_str_record)

        # 버스 설정
        bus = self.pipeline.get_bus()
        bus.add_signal_watch()

        # GObject 메인 루프 및 GLib 메인 컨텍스트 생성
        self.loop = GLib.MainLoop()

        # 메시지 처리 함수
        def on_message(bus, message):
            if message.type == Gst.MessageType.EOS:
                print("End of stream")
                self.loop.quit()
            elif message.type == Gst.MessageType.ERROR:
                err, debug = message.parse_error()
                print(f"Error: {err}, {debug}")
                self.loop.quit()
                raise Exception
                

        # 메시지 핸들러 연결
        bus.connect("message", on_message)

        # 파이프라인 시작
        self.pipeline.set_state(Gst.State.PLAYING)

        def check_for_stop():
            if self.stop_event.is_set():
                print("Stop event detected, sending EOS...")
                self.pipeline.send_event(Gst.Event.new_eos())
                return False  # Stop the timeout function
            return True  # Continue the timeout function

        # 일정 간격으로 stop_event를 체크
        GLib.timeout_add(1, check_for_stop)

        # GStreamer 파이프라인을 실행하기 위한 메인 루프 실행
        try:
            self.loop.run()
        finally:
            # 파이프라인 정지
            self.pipeline.set_state(Gst.State.NULL)
            print("Pipeline stopped.")

    def start(self):
        # 폴더 생성 (폴더가 없으면 생성)
        os.makedirs(os.path.dirname(self._file_name), exist_ok=True)

        if self.stop_event.is_set():
            self.stop_event.clear()

        # GStreamer 파이프라인을 실행할 별도의 프로세스 생성
        self.process = threading.Thread(target=self._gstreamer_pipeline)
        self.process.start()

    def stop(self):
        # 종료 이벤트 설정 및 프로세스 종료 대기
        self.stop_event.set()
        self.process.join()

if __name__ == '__main__':
    Gst.init(None)
    client = RTSPRecord(EO, RTSP_IP)
    print(client.checkCam())
    client.start()
    time.sleep(10)
    client.stop()