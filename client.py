import socket
import json

GROUP = "Ethernautas_v2"

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

            message = {
                "group": GROUP,
                "payload": payload
            }
            client.sendall(json.dumps(message).encode("utf-8"))
            print(f"Enviado: {message}")
    except (KeyboardInterrupt, BrokenPipeError):
        print("\nConexión cerrada.")
    finally:
        client.close()

if __name__ == "__main__":
    main()