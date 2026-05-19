# TP N4: Infraestructura de servicios web con perspectiva de redes

### Integrantes
- Costamagna, Matias Javier
- de la Mata, Nicolas
- Quispe, Mateo
- Sabena, Maria Pilar

---

## Consigna 1

### a) ¿Qué es la serialización en redes de computadoras?

La **serialización** es el proceso de convertir una estructura de datos u objeto (residente en memoria) en una secuencia lineal de bytes o caracteres que puede ser transmitida a través de una red y reconstruida posteriormente por el receptor (**deserialización**).

En redes, esto es necesario porque los datos en memoria tienen referencias, punteros y formatos específicos de cada arquitectura o lenguaje que no son directamente transmisibles. La serialización los transforma en un formato portable y autocontenido que viaja como carga útil dentro de los paquetes de la capa de transporte. Sin serialización, dos programas escritos en distintos lenguajes o corriendo en distintas arquitecturas no podrían intercambiar estructuras de datos de forma interoperable.

---

### b) Diferencia entre serialización binaria y no binaria

| | **Binaria** | **No binaria (textual)** |
|---|---|---|
| **Formato** | Bytes crudos, no legible por humanos | Texto plano (ASCII/UTF-8) |
| **Ejemplos** | Protocol Buffers (protobuf), MessagePack, BSON, Avro | JSON, XML, YAML, CSV |
| **Ventajas** | Compacta (menor tamaño en bytes), más rápida de serializar/deserializar, eficiente para tipos numéricos y datos binarios nativos | Legible por humanos, fácil de depurar e inspeccionar, interoperable sin herramientas especiales, ampliamente soportada |
| **Desventajas** | Difícil de inspeccionar sin herramientas, menor interoperabilidad sin un esquema compartido, más compleja de implementar | Mayor tamaño en bytes, más lenta de parsear, tipos ambiguos (ej: JSON no distingue entero de flotante en todos los contextos) |

**Ejemplos concretos:**

- *JSON (no binario):* `{"group": "ethernautas", "payload": "hola"}` — transmitido exactamente como ese texto. Readable en Wireshark sin ningún procesamiento adicional.
- *Protocol Buffers (binario):* el mismo mensaje se codifica en ~15 bytes de datos compactos con campos identificados por número, ilegibles directamente pero mucho más eficientes en ancho de banda.

**En el contexto del TP:** se usa JSON, serialización **no binaria**. Esto facilita verificar los mensajes directamente en Wireshark o PacketSender sin herramientas adicionales, a costa de un mayor tamaño de paquete.

---

## Consigna 2

Se desplegó un servidor TCP multi-hilo implementado en Python (`server.py`). El servidor escucha en `0.0.0.0:5000` y atiende cada cliente en un hilo independiente, permitiendo conexiones simultáneas.

### a) Envío de mensajes con PacketSender

Los mensajes se serializaron en JSON con la morfología requerida:

```json
{
    "group": "Ethernautas_v2",
    "payload": "<mensaje/carga_útil>"
}
```

Se utilizó **PacketSender** en modo TCP persistente (opción *Persistent TCP*) para mantener la conexión abierta entre envíos y verificar que los mensajes llegaban correctamente al servidor.

![PacketSender conectado al servidor](assets/packetsender_connected.png)

El servidor validó el formato del mensaje y lo mostró por consola con el nombre del grupo remitente. En caso de recibir un mensaje con formato incorrecto o que no pudiera deserializarse como JSON, el servidor respondía con un aviso de mensaje mal formado.

---

## Consigna 3

Se implementó una aplicación de cliente en Python (`client.py`) que permite enviar mensajes al servidor desde la consola de forma interactiva.

### a) Configuración de IP y puerto

Al ejecutarse, el cliente solicita al usuario la IP y el puerto del servidor, establece una conexión TCP y mantiene la sesión abierta mientras el usuario envíe mensajes:

```
IP del servidor: 127.0.0.1
Puerto del servidor: 5000
Conectado a 127.0.0.1:5000. Escribí tu mensaje (o 'exit' para salir).
```

### b) Serialización de mensajes

Antes de enviar cada mensaje, el cliente lo empaqueta en el formato JSON que el servidor admite, codificándolo en UTF-8:

```python
message = {"group": GROUP, "payload": payload}
client.sendall(json.dumps(message).encode("utf-8"))
```

El campo `group` se fija en `"Ethernautas_v2"` y `payload` contiene el texto ingresado por el usuario.

### c) Verificación del funcionamiento

Se ejecutaron servidor y cliente en paralelo en la misma máquina (`127.0.0.1:5000`). El servidor recibió y mostró correctamente cada mensaje enviado desde el cliente:

![Servidor y cliente en funcionamiento](assets/client_server_demo.png)

---

## Consigna 4

Se implementó cifrado **Fernet** sobre la payload del mensaje, dejando el campo `group` en texto claro.
 
### a) Cifrado en el cliente
 
Se utilizó la librería `cryptography` de Python. Una clave fija generada con `Fernet.generate_key()` se hardcodea en el cliente. Antes de serializar el mensaje, la payload se cifra:
 
```python
from cryptography.fernet import Fernet
 
KEY = b"<clave_generada>"
fernet = Fernet(KEY)
 
encrypted_payload = fernet.encrypt(payload.encode("utf-8")).decode("utf-8")
 
message = {
    "group": GROUP,
    "payload": encrypted_payload
}
```
 
### b) Verificación
 
El servidor recibe la payload completamente cifrada e ilegible. En la captura se observa que el campo `group` llega en claro (`EthernautasV2`) mientras que la payload es texto cifrado en base64:
 
![Cliente cifrando y servidor recibiendo payload cifrada](assets/fernet.png)
 
### c) Características de Fernet
 
- **Tipo:** Cifrado simétrico — la misma clave cifra y descifra.
- **Algoritmo subyacente:** AES-128 en modo CBC para el cifrado, con HMAC-SHA256 para verificar integridad.
- **Formato de salida:** Base64 URL-safe, lo que lo hace directamente embebible en un JSON.
- **Propiedad destacada:** Cada cifrado del mismo texto produce un resultado diferente (usa un IV aleatorio), por lo que no es posible detectar mensajes repetidos analizando el tráfico.
- **Librería:** `cryptography` (Python) — `pip install cryptography`.
