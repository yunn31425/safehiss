import socket
import packet
import struct

def create_command():
    # 이 예제는 HDMI 출력을 활성화하는 명령을 나타냅니다.
    # 실제 명령은 ZT6 SDK 문서에서 찾아야 합니다.
    singlePacket = packet.packet()
    singlePacket.ctrl = 1
    singlePacket.seq = 1
    singlePacket.cmd_id = 0x00
    singlePacket.data = []
    singlePacket.data = [0x19]

    command = singlePacket.pack()

    data = 0x55 + 0x66 + 0x01 + 0x00 + 0x00 + 0x00 + 0x00 + 0x19 + 0x5D + 0x57
    command = struct.pack('<BBBBBBBBBB', 0x55 , 0x66 , 0x01 , 0x00 , 0x00 , 0x00 , 0x00 , 0x19 , 0x5D , 0x57)
    
    print(command)



    return command

def send_udp_command(ip, port, command):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # UDP 소켓 생성
    sock.settimeout(2)  # 타임아웃 설정 (2초)

    try:
        sock.sendto(command, (ip, port))  # 명령 전송
        response, addr = sock.recvfrom(1024)  # 응답 수신
        print(f"응답: {response} from {addr}")
    except socket.timeout:
        print("응답 시간 초과")
    finally:
        sock.close()

if __name__ == "__main__":
    ip = "192.168.144.25"  # ZT6의 IP 주소
    port = 37260  # ZT6의 UDP 포트 번호 (실제 포트 번호로 변경 필요)

    command = create_command()
    send_udp_command(ip, port, command)
