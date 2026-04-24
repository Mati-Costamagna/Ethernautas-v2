# TP N3: Introducción a infraestructura de servicios web con perspectiva de redes

### Integrantes
- Costamagna, Matias Javier
- de la Mata, Nicolas
- Quispe, Mateo
- Sabena, Maria Pilar

---

## Consigna 1 

### a) ¿Qué es SSH y qué problema resuelve?

**SSH** (*Secure Shell*) es un protocolo de red que permite acceder y administrar de forma segura un equipo remoto a través de una red insegura (como Internet).

Resuelve el problema de la **transmisión de datos en texto plano** que tenían protocolos anteriores como Telnet o rlogin. Con esos protocolos, cualquier persona que pudiera interceptar el tráfico de red (ataque de *sniffing*) podía leer comandos, contraseñas y toda la información transmitida. SSH soluciona esto estableciendo un **canal cifrado** entre cliente y servidor antes de intercambiar cualquier dato.

---

### b) Diferencia entre autenticación y cifrado

Aunque suelen trabajar juntos, son conceptos distintos:

| Concepto | ¿Qué garantiza? | Pregunta que responde |
|---|---|---|
| **Autenticación** | Que la entidad es quien dice ser | *¿Con quién estoy hablando?* |
| **Cifrado** | Que el contenido no puede ser leído por terceros | *¿Puede alguien más leer esto?* |

- **Autenticación** es el proceso de verificar la identidad de un usuario o sistema. En SSH, esto ocurre cuando el servidor verifica que el cliente que intenta conectarse es legítimo (por clave pública o contraseña). Stallings lo encuadra dentro de los servicios de seguridad como *autenticación de entidad par*.

- **Cifrado** (o encriptación) es la transformación de datos en texto plano a texto cifrado, de modo que solo quien posea la clave correcta pueda revertir el proceso y leerlos. Stallings lo trata en el contexto de la *confidencialidad*, uno de los pilares de la seguridad en redes.

> En SSH, **primero se autentica** y **luego se cifra** (nadie más puede leer lo que nos decimos).

---

### c) ¿Qué es una clave pública y una clave privada?

Son el par de claves usadas en la **criptografía asimétrica** (o de clave pública), descripta por Stallings como uno de los avances fundamentales en criptografía moderna.

- **Clave privada:** Es un valor secreto que solo posee su dueño. Nunca se comparte. Se usa para **firmar** o **descifrar** mensajes.

- **Clave pública:** Es derivada matemáticamente de la privada, pero no permite deducir la privada a partir de ella. Se puede distribuir libremente. Se usa para **verificar firmas** o **cifrar** mensajes dirigidos al dueño de la clave privada.

**¿Cómo funciona el principio?**  
Si alguien cifra un mensaje con tu clave pública, **solo tú** (con tu clave privada) podrás descifrarlo. Si tú firmas algo con tu clave privada, **cualquiera** con tu clave pública puede verificar que fue tuyo.

---

### d) ¿Por qué la clave privada no debe compartirse?

La clave privada es el **único secreto** que garantiza la identidad de su dueño. Si alguien más la obtiene:

1. **Puede hacerse pasar por vos** ante cualquier servidor que confíe en tu clave pública.
2. **Puede descifrar todos los mensajes** que te fueron enviados cifrados con tu clave pública.
3. **La autenticación pierde todo su valor**: ya no hay forma de distinguir al legítimo dueño de un impostor.

Stallings señala que en los sistemas de clave pública, la seguridad del esquema completo depende de que la clave privada permanezca secreta. A diferencia de la clave pública (cuya distribución es deseable), la exposición de la clave privada compromete irreversiblemente la seguridad del sistema para ese par de claves.

> En la práctica: si se sospecha que una clave privada fue comprometida, debe **revocarse y reemplazarse** inmediatamente.

---

### e) ¿Qué ventajas tienen las claves SSH frente a contraseñas?

| Criterio | Contraseña | Clave SSH |
|---|---|---|
| **Transmisión por red** | Aunque cifrada en SSH, se envía al servidor | La clave privada **nunca** sale del cliente |
| **Susceptibilidad a fuerza bruta** | Alta, especialmente si es corta o predecible | Extremadamente baja (clave de 2048–4096 bits) |
| **Phishing** | Puede ser capturada en sitios falsos | No aplica: el servidor debe conocer la clave pública previamente |
| **Automatización segura** | Requiere intervención humana o almacenamiento inseguro | Se pueden usar sin intervención humana de forma segura |
| **Reutilización** | Muchos usuarios repiten contraseñas | Cada par de claves es único |

La ventaja más importante desde el punto de vista de Stallings es que con claves SSH se implementa un esquema de **autenticación de desafío-respuesta** basado en criptografía asimétrica: el servidor envía un desafío cifrado con la clave pública del usuario, y solo quien posee la clave privada puede responderlo correctamente. Esto significa que **la información secreta nunca viaja por la red**, eliminando la posibilidad de capturarla mediante sniffing o ataques de repetición (*replay attacks*).

---

## Consigna 2

### Verificación de conexión SSH a la VM

Para verificar la conexión SSH a la VM se utilizó el siguiente comando:

```bash
ssh -i ./pc3_key.pem pc-alumnos-3@4.206.219.90
```

![Conexión SSH y creación de carpeta](assests/pc3_connection.png)

Una vez conectados, se creó la carpeta del grupo dentro de la VM:

```bash
mkdir ethernautas_v2
```

La captura muestra la conexión exitosa al sistema Debian GNU/Linux (kernel 6.1.0-44-cloud-amd64) y la carpeta `ethernautas_v2` creada correctamente.

---

## Consigna 3

### Captura de tráfico SSH con Wireshark

Se configuró Wireshark para capturar el tráfico hacia la IP de la VM y se inició una sesión SSH. El filtro utilizado fue:

```
ip.dst == 4.206.219.90
```

![Paquetes SSH capturados en Wireshark](assests/pc3_ssh_package.png)

**¿Se puede descifrar el contenido?**

No. Como se observa en la captura, todos los paquetes SSH aparecen como `Client: Encrypted packet` o `Server: Encrypted packet`. SSH establece un canal cifrado (en este caso con AES-256-CTR) **antes** de transmitir cualquier dato de usuario. Wireshark puede ver los metadatos del paquete (IPs, puertos, longitudes) pero el payload es completamente ilegible sin la clave de sesión.

**¿Es la clave `.pem` la que cifra este tráfico?**

No. El par de claves pública/privada (el archivo `.pem`) cumple un rol exclusivo de **autenticación**: le demuestra al servidor que quien se conecta es el legítimo dueño de la clave privada. El cifrado del tráfico en sí se realiza con una clave de sesión distinta, generada durante el handshake. La clave pública viaja en ese proceso, pero la clave de sesión resultante nunca se transmite por la red, por lo que no puede capturarse con Wireshark.

---

## Consigna 4

### a) Servidor TCP con ncat

Se montó un servidor TCP en la VM escuchando en el puerto `5432`:

```bash
# En la VM (servidor)
sudo ncat -l 5432

# En la PC local (cliente)
ncat 4.206.219.90 5432
```

Se configuró Wireshark con el filtro `ip.dst == 4.206.219.90 and !ssh` para capturar únicamente el tráfico TCP no SSH hacia la VM.

**Three-way handshake y mensajes:**

![Handshake TCP capturado en Wireshark](assests/pc3_handshake.png)

![Tráfico TCP - parte 1](assests/pc3_tcp_p1.png)

![Tráfico TCP - parte 2](assests/pc3_tcp_p2.png)

La captura muestra el handshake completo (SYN → SYN-ACK → ACK) seguido del intercambio de mensajes entre la PC local y la VM. **El contenido es completamente legible en texto plano** tanto en la vista de paquetes como en el panel de bytes de Wireshark: no hay ningún tipo de cifrado en esta comunicación.

---

### b) Servidor UDP con ncat

Se repitió el ejercicio usando protocolo UDP. ncat requiere el flag `-u` tanto en servidor como en cliente:

```bash
# En la VM (servidor)
sudo ncat -u -l 5432

# En la PC local (cliente)
ncat -u 4.206.219.90 5432
```

![Tráfico UDP capturado - parte 1](assests/pc3_udp_p1.png)

![Tráfico UDP capturado - parte 2](assests/pc3_udp_p2.png)

**Diferencias observadas respecto a TCP:**

- UDP **no realiza handshake**: los datos se envían directamente sin establecer conexión previa. En la captura se observa que no hay paquetes SYN/SYN-ACK/ACK.
- Los mensajes son igualmente **visibles en texto plano** en el análisis de bytes de Wireshark.
- UDP es un protocolo *connectionless*: no garantiza entrega, orden ni detección de errores a nivel de transporte.

---

### c) Chat ncat entre dos VMs

> **Pendiente**: abrir dos sesiones SSH simultáneas (una a pc3 en Azure y otra a pc4 en Google), levantar ncat en una como servidor y conectarse desde la otra, y documentar el intercambio de mensajes entre ambas instancias.

---

## Consigna 5

### Servidor HTTP con Python

Dentro de la carpeta del grupo en la VM, se creó el archivo `index.html` y se desplegó un servidor HTTP:

```bash
cd ethernautas_v2
python3 -m http.server 5000
```

El mismo procedimiento se realizó en ambas VMs. Desde el navegador se accedió a cada una y se verificó el acceso:

**VM pc3 (Azure — `4.206.219.90`):**

![Página servida por HTTP desde pc3](assests/pc3_https_p1.jpeg)

**VM pc4 (Google — `34.148.193.117`):**

![Página servida por HTTP desde pc4](assests/pc4_http_p1.png)

Se capturó el tráfico HTTP con Wireshark usando el filtro `ip.dst == 34.148.193.117 and !ssh`:

![Tráfico HTTP capturado en Wireshark](assests/pc4_http_wireshark.png)

**¿Se puede descifrar el contenido HTTP?**

Sí. HTTP transmite todo en **texto plano**. En Wireshark se puede ver íntegramente el request (`GET / HTTP/1.1`) y el response con el HTML completo del `index.html`. No hay cifrado de ningún tipo.

**¿Se podría intervenir el contenido?**

Sí. Al tratarse de HTTP sin TLS, cualquier nodo intermedio en la ruta de red (router, ISP, atacante en la misma red) podría realizar un ataque **Man-in-the-Middle (MitM)**: interceptar la respuesta del servidor y modificar el HTML antes de que llegue al cliente, sin que ninguna de las partes lo detecte. Esto es precisamente el problema que resuelve HTTPS: al cifrar el canal con TLS, cualquier modificación en tránsito invalida la firma del certificado y el cliente rechaza la conexión.

---

## Consigna 6

> **Pendiente**: ver el video de Veritasium y responder los puntos a) y b).
