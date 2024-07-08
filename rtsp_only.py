import cv2
import av
import numpy as np

# 비디오 캡처 초기화 (0은 기본 웹캠을 의미)
rtsp_url = "rtsp://192.168.144.25:8554/video1"
cap = cv2.VideoCapture(rtsp_url)

# PyAV로 H.264 인코더 설정
output_container = av.open('output.mp4', mode='w', format='mp4')
stream = output_container.add_stream('h264', rate=30)
stream.width = 640
stream.height = 480
stream.pix_fmt = 'yuv420p'

while True:
    ret, frame = cap.read()
    if ret:
        # 프레임을 PyAV 패킷으로 인코딩
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame_av = av.VideoFrame.from_ndarray(frame_rgb, format='rgb24')
        packet = stream.encode(frame_av)

        # 인코딩된 프레임을 디코딩하여 화면에 표시
        if packet:
            for frame in packet:
                img = frame.to_ndarray(format='bgr24')
                cv2.imshow('frame', img)
    else:
        break

# 모든 리소스 해제
cap.release()
output_container.close()
cv2.destroyAllWindows()
