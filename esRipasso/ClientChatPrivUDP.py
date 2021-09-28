import socket as sck
import threading as thr

ADDRESS=("192.168.0.126", 5000)


class Receiver(thr.Thread):
    def __init__(self):
        thr.Thread.__init__(self) #super di Java
        self.running=True
    def run(self):
        while self.running:
            received_msg, _ = s.recvfrom(4096)
            print(f"\n{received_msg.decode()}")


def main():
    global s
    s = sck.socket(sck.AF_INET, sck.SOCK_DGRAM)

    nick_name = input("Inserisci il tuo nickname: ")
    s.sendto(f"Nickname\n{nick_name}".encode(), ADDRESS)


    data, _ = s.recvfrom(4096)       #ok
    print(data.decode())



    receiver=Receiver()
    receiver.start()

    
    while True:

        destinatario = input("Inserisci il nickname del destinatario: ")
        msg = input("Inserisci il messaggio da inviare: ")
        s.sendto(f"{nick_name}\n{destinatario}\n{msg}".encode(), ADDRESS)

        if msg=="exit":
            receiver.running=False
            receiver.join()
            break

if __name__=="__main__":
    main()

