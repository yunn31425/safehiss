import socket
import packet
import struct

def create_command():

    singlePacket = packet.packet()
    singlePacket.ctrl = 1
    singlePacket.seq = 0x1D
    singlePacket.cmd_id = 0x12
    singlePacket.data = [0x40, 0x01, 0x00, 0x01, 0x01]

    command = singlePacket.pack()

    return command

def send_udp_command(ip, port, command):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # UDP 소켓 생성
    sock.settimeout(10)  # 타임아웃 설정 (2초)

    try:
        sock.sendto(command, (ip, port))  # 명령 전송
        response, addr = sock.recvfrom(1024)  # 응답 수신
        print(f"응답: {response.hex()} from {addr}")
        data = list(hex(i) for i in response)
        print(data)
    except socket.timeout:
        print("응답 시간 초과")
    finally:
        sock.close()

if __name__ == "__main__":
    ip = "192.168.144.25"  # ZT6의 IP 주소
    port = 37260  # ZT6의 UDP 포트 번호 (실제 포트 번호로 변경 필요)

    command = create_command()
    send_udp_command(ip, port, command)
