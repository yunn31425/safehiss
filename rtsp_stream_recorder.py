import cv2
import datetime

'''

Press 1 : 4K image
Press 2 : Thermal image
Press ESC : Close

'''


def get_rtsp_url(choice):
    if choice == 1:
        return 'rtsp://192.168.144.25:8554/video1'
    elif choice == 2:
        return 'rtsp://192.168.144.25:8554/video2'
    return None

def writeVideo():
    current_stream = None
    video_capture = None
    out = None
    
    while True:
        if current_stream is None:
            choice = int(input("Select the video stream (1 or 2): "))
            rtsp_url = get_rtsp_url(choice)
            if rtsp_url is not None:
                current_stream = choice
                video_capture = cv2.VideoCapture(rtsp_url)
                video_capture.set(3, 800)
                video_capture.set(4, 600)
                fps = 20
                streaming_window_width = int(video_capture.get(3))
                streaming_window_height = int(video_capture.get(4))
                currentTime = datetime.datetime.now()
                fileName = str(currentTime.strftime('%Y %m %d %H %M %S'))
                path = f'D:/cctv/cctv/python/{fileName}.avi'
                fourcc = cv2.VideoWriter_fourcc('X', 'V', 'I', 'D')
                out = cv2.VideoWriter(path, fourcc, fps, (streaming_window_width, streaming_window_height))

        ret, frame = video_capture.read()
        if ret:
            cv2.imshow('streaming video', frame)
            out.write(frame)
        
        k = cv2.waitKey(1) & 0xFF
        if k == 27:  # ESC key to break
            break
        elif k == ord('1') or k == ord('2'):
            new_choice = int(chr(k))
            if new_choice != current_stream:
                current_stream = new_choice
                rtsp_url = get_rtsp_url(current_stream)
                if rtsp_url is not None:
                    video_capture.release()
                    out.release()
                    cv2.destroyAllWindows()
                    video_capture = cv2.VideoCapture(rtsp_url)
                    video_capture.set(3, 800)
                    video_capture.set(4, 600)
                    streaming_window_width = int(video_capture.get(3))
                    streaming_window_height = int(video_capture.get(4))
                    currentTime = datetime.datetime.now()
                    fileName = str(currentTime.strftime('%Y %m %d %H %M %S'))
                    path = f'D:/cctv/cctv/python/{fileName}.avi'
                    fourcc = cv2.VideoWriter_fourcc('X', 'V', 'I', 'D')
                    out = cv2.VideoWriter(path, fourcc, fps, (streaming_window_width, streaming_window_height))
                    
    if video_capture is not None:
        video_capture.release()
    if out is not None:
        out.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    writeVideo()
