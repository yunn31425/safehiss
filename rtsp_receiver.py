import cv2
import time

def main():
    # Replace this with your RTSP stream URL
    # rtsp_url = "rtsp://your_ip_address:port/your_stream"
    rtsp_url = "rtsp://192.168.144.25:8554/video2"

    # Open the RTSP stream
    cap = cv2.VideoCapture(rtsp_url)

    if not cap.isOpened():
        print("Error: Could not open RTSP stream.")
        return
    

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error: Could not read frame.")
            break

        # Display the frame

        cv2.imshow("RTSP Stream", frame)

    # Release the capture and close any OpenCV windows
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
