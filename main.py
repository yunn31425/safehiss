from button.osbutton import *
from lcd.lcdApi import *
from siyi.cam import *
from Lidar.Lidar_recode import *
import threading, sys, time, subprocess

SERVER_URL = 'http://203.255.57.124:5000'
RTSP_VISIBLE_URL = "rtsp://192.168.144.25:8554/video1"
RTSP_THERMAL_URL = "rtsp://192.168.144.25:8554/video2"
RTSP_IP = "192.168.144.25"


if __name__ == '__main__':
    lcdProjetor = EasyLcd()
    print(lcdProjetor)
    lcdProjetor.lcd_init()
    lcdProjetor.lcd_string_up("--INITIALIZING--")

    # cam 초기화
    try:
        visible_cam = camClient(SERVER_URL, RTSP_VISIBLE_URL, RTSP_IP)
        thermal_cam = camClient(SERVER_URL, RTSP_THERMAL_URL, RTSP_IP)
        lcdProjetor.lcd_string_down("CAM : ")

        cam_check_result = visible_cam.checkCam()
        if cam_check_result:
            lcdProjetor.lcd_string_down("CAM : OK")
        else:
            lcdProjetor.lcd_string_down("CAM : CAM FAIL")
            lcdProjetor.lcd_string_up("PLEASE REBOOT")
            sys.exit()
    except PermissionError:
        lcdProjetor.lcd_string_down("CAM FAIL : PRM")
        lcdProjetor.lcd_string_up("PLEASE REBOOT")
        sys.exit()
    
    time.sleep(1)
    
    # 라이다 초기화
    try:
        lcdProjetor.lcd_string_down("Lidar : ")
        lidar_module = Lidar_recoder()
        lidar_check_result = lidar_module.checkConnection()

        if lidar_check_result:
            lcdProjetor.lcd_string_down("Lidar : OK")
            time.sleep(1)
    except PermissionError:
        lcdProjetor.lcd_string_down("Lidar FAIL : PRM")
        lcdProjetor.lcd_string_up("PLEASE REBOOT")
        sys.exit()

    # SSD 용량 조회
    check_avail_space_order = ['df', '-h']

    df_process = subprocess.Popen(check_avail_space_order, stdout=subprocess.PIPE)

    # 두 번째 명령어 실행 (grep '/dev/nvme0n1p1') - 첫 번째 명령어의 출력을 입력으로 사용
    grep_process = subprocess.Popen(['grep', '/dev/nvme0n1p1'], stdin=df_process.stdout, stdout=subprocess.PIPE)

    # 첫 번째 명령어의 출력을 닫아줌
    df_process.stdout.close()

    # 최종 결과 읽기
    avail_space_result, _ = grep_process.communicate()
    
    print(avail_space_result)

    avail_space_result_split = str(avail_space_result).split(" ")

    print(avail_space_result_split[10])

    if int(avail_space_result_split[10][:-1]) > 90:
        lcdProjetor.lcd_string_up("NOT ENOUGH SPACE")
        lcdProjetor.lcd_string_up("PLZ EMPTY SPACE")
        sys.exit()
        

    # 초기화 완료
    lcdProjetor.lcd_init()
    lcdProjetor.lcd_string_up("INIT COMPLETE")

    time.sleep(1)

    lcdProjetor.lcd_string_up("READY FOR RECORD")

    gpio_id = 391
    gpio_index = "PH.00"

    # GPIOController 객체 생성
    gpio = GPIOController(gpio_id, gpio_index)

    if_recording = False

    eo_recorder = RTSPRecord(1, RTSP_IP)
    ir_recorder = RTSPRecord(2, RTSP_IP)

    try:
        gpio.unexport()
        gpio.export()
        gpio.set_direction("in")

        while True:
            try: 
                if gpio.check_pushed():
                    if if_recording:
                        lcdProjetor.lcd_string_up("STOP RECORD")
                        lcdProjetor.lcd_string_down("SAVING")
                        ir_file_name, ir_directory = ir_recorder.stop()
                        eo_file_name, eo_directory = eo_recorder.stop()
                        lidar_module.stop()

                        print(eo_file_name, eo_directory)
                        print(ir_file_name, ir_directory)
                        
                        lcdProjetor.lcd_string_down("SAVING COMPLETE")

                        time.sleep(2)

                        lcdProjetor.lcd_init()

                        lcdProjetor.lcd_string_up("READY FOR RECORD")

                        if_recording = False
                        
                    else:
                        start_time = time.time()
                        
                        eo_recorder.update_file_name()
                        ir_recorder.update_file_name()
                        
                        lcdProjetor.lcd_string_up("START RECORDING")
                        eo_recorder.start()
                        ir_recorder.start()
                        lidar_module.start()
                        
                        if_recording = True
                        
                if if_recording:
                    gap = int(time.time() - start_time)
                    lcdProjetor.lcd_string_down(f"REC {str(gap//3600).zfill(2)}:{str(gap//60 - gap//3600).zfill(2)}:{str(gap%60).zfill(2)}")

            except Exception as e:
                print('---ERROR---', e)
                lcdProjetor.lcd_init()
                lcdProjetor.lcd_string_up("---ERROR---")
                sys.exit()

            time.sleep(0.1)
    except Exception as e:
        print(e)
        lcdProjetor.lcd_init()
        lcdProjetor.lcd_string_up("---ERROR---")

    finally:
        # GPIO 해제 (unexport)
        gpio.cleanup()
        print(f"GPIO {gpio_index} has been unexported.")
