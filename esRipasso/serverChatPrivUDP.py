import socket as sck
#import threading as thr

ADDRESS=("127.0.0.1", 1123)

nnDict={}
OK = "ok"

def main():
    global nnDict
    s = sck.socket(sck.AF_INET,sck.SOCK_DGRAM)
    s.bind(ADDRESS)

    while True:
        data, address=s.recvfrom(4096)
        received_msg= data.decode()
        msg=received_msg.split(":")

        if msg[0].lower()=="nickname":              #messaggio di hello
            nnDict[msg[1]] = address
            s.sendto(OK.encode(), address)
        else:
            for k in nnDict.keys():
                if k == msg[1]:
                    print(f"{msg[0]} manda a {msg[1]}: {msg[2]}")
                    s.sendto(msg[2].encode(),nnDict[k])
            
        if msg[2]!="exit":
            msg=received_msg.split(":")
            #print(f"{msg[0]} ha scritto a {msg[1]}: {msg[2]}")
            for user in nnDict.keys():
                if user==msg[1]:
                    s.sendto(received_msg.encode(), nnDict[user])
        else:
            for val in nnDict.values():
                if val == address:
                    nnDict.popitem(val)

if __name__=="__main__":
    main()