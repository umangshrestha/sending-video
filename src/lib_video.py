from socket import (
    socket,
    SOCK_STREAM,
    AF_INET,
    SO_REUSEADDR,
    SOL_SOCKET,
    error,
    timeout
)
from multiprocessing import Process
import cv2
import traceback
from settings import Port, Ip
from lib_pack import (
    cv_pack,
    cv_unpack
)


__all__ = [
    "Client",
    "Server"
]

class Client(Process):
    '''
    Client does following task:
    1. records data from camera 
    3. parse cv data to bytes
    2. send data through tcp socket
    '''
    def __init__(self, ip=Ip, port=Port):
        super(Client, self).__init__()
        self.cap = None
        self.Flag = True
        self.client_socket = socket(AF_INET, SOCK_STREAM)
        self.client_socket.connect((ip, port))


    def run(self):
        self.cap = cv2.VideoCapture(0)
        while self.Flag:
            try:
                ret, frame = self.cap.read()
                data = cv_pack(frame)
                self.client_socket.sendall(data)
            except (
                BrokenPipeError, 
                ConnectionResetError,
                ConnectionRefusedError
            ) as E:
                break
            except Exception as E:
                print("exception:", E)
                traceback.print_stack()

    def stop(self):
        self.flag = False

    def __del__(self):
        if self.client_socket:
            self.client_socket.close()
        if self.cap:
            self.cap.release()
        cv2.destroyAllWindows()


class Server(Process):
    '''
    Server does following tasks:
    1. recieve data  from tcp socket
    2. parse bytest to cv 
    3. display the data
    '''
    def __init__(self, port=Port):
        super(Server, self).__init__()
        self.Flag = True
        self.server_socket = socket(AF_INET, SOCK_STREAM)
        self.server_socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        self.server_socket.bind(("", port))
        self.server_socket.listen(1)

    def run(self):
        conn, address = self.server_socket.accept()
        data = b''
        while self.Flag:
            try:
                '''
                old logic:
                packed_msg_size = data[:payload_size]
                data = data[payload_size:]
                msg_size = unpack(packed_msg_size)
                while len(data) < msg_size:
                    data += conn.recv(4096)
                frame_data = data[:msg_size]
                data = data[msg_size:]
                frame = pickle.loads(frame_data)
                cv2.imshow('frame', frame)
                '''
                
                data += conn.recv(9076)
                frame = cv_unpack(data)
                if frame.end_pos == -1:
                    continue
                cv2.imshow('frame', frame.data)
                data = data[frame.end_pos:]

                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
            except Exception as E:
                print("exception:", E)
                traceback.print_stack()

    def stop(self):
        self.Flag = False

    def __del__(self):
        cv2.destroyAllWindows()
        self.server_socket.close()


if __name__ == "__main__":
    # Server needs to be started before 
    # client else we get "ConnectionRefusedError"
    s = Server()
    s.start()
    
    c = Client()
    c.start()

