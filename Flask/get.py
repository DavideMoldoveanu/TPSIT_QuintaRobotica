import time
import socket as sck


def main():
    target = "www.google.com"
    port = 80

    client = sck.socket(sck.AF_INET, sck.SOCK_STREAM)
    client.connect((target, port))

    