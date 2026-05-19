import socket
import json
from cryptography.fernet import Fernet
 
GROUP = "EthernautasV2"
 
# Generada con Fernet.generate_key() — compartir con el servidor para el descifrado
KEY = b'l8U8GsZHvMg02wKlbGHf8EmkwfNs2GYvGgMTrOQSq2U='
fernet = Fernet(KEY)
 
def encrypt_payload(payload: str) -> str:
    return fernet.encrypt(payload.encode("utf-8")).decode("utf-8")
 
def main():
    host = input("IP del servidor: ").strip()
    port = int(input("Puerto del servidor: ").strip())
 
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((host, port))
    print(f"Conectado a {host}:{port}. Escribí tu mensaje (o 'exit' para salir).")
 
    try:
        while True:
            payload = input("> ")
            if payload.lower() == "exit":
                break
 
            encrypted_payload = encrypt_payload(payload)
 
            message = {
                "group": GROUP,
                "payload": encrypted_payload
            }
 
            client.sendall(json.dumps(message).encode("utf-8"))
            print(f"Payload original:  {payload}")
            print(f"Payload cifrada:   {encrypted_payload}")
            print(f"Mensaje enviado:   {message}\n")
    except (KeyboardInterrupt, BrokenPipeError):
        print("\nConexión cerrada.")
    finally:
        client.close()
 
if __name__ == "__main__":
    main()
