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
## Consigna 2
Para verificar la conexión SSH a la VM se utilizó el siguiente comando:
``` ssh -i <path/a/la/clave> <usuario>@<ip> ``` 

[Conexión SSH a la VM]

Una vez conectados, se creó la carpeta del grupo dentro de la VM:
``` mkdir Ethernautas``` 

[Carpeta en la VM]
## Consigna 3
Se configuró Wireshark para capturar el tráfico hacia la IP de la VM y se inició una sesión SSH. El filtro utilizado fue:
``` ip.dst == <VM_IP> ```

[Paquetes SSH capturados]

*¿Se puede descifrar el contenido?*
No. Como se observa en la captura, todos los paquetes SSH aparecen como Encrypted packet. SSH establece un canal cifrado desde el inicio de la sesión , por lo que todo el contenido viaja cifrado. Wireshark puede ver que existe tráfico entre los hosts, pero no puede revelar su contenido.
## Consigna 4
a) Servidor TCP con netcat
Se montó un servidor TCP en la VM escuchando en un puerto habilitado:
` En la VM (servidor) 
ncat -l <puerto> `

Se configuró Wireshark con el filtro ip.dst == <VM_IP> and !ssh para capturar únicamente el tráfico TCP no SSH.
Desde la computadora local se conectó al servidor:

``` En la PC local (cliente)
ncat <VM_IP> <PUERTO> ```

[Handshake TCP capturado en Wireshark]

Una vez establecida la conexión, se enviaron mensajes entre ambos extremos:

[acá foto de los mensajes enviados]

b) Servidor UDP con netcat
Se repitió el procedimiento anterior pero usando el protocolo UDP. Para enviar tráfico UDP con netcat se utiliza el flag -u:
``` En la VM (servidor)
ncat -u -l <puerto> ```

``` En la PC local (cliente)
ncat -u <VM_IP> <PUERTO> ```

## Consigna 5
Servidor HTTP con Python
Dentro de la carpeta del grupo creada en la consigna 2, se creó un archivo index.html.
Se levantó un servidor HTTP simple con Python:
``` python3 -m http.server 8000 ```
Desde el navegador de la PC local se accedió a http://<VM_IP>:8000 y se verificó el acceso:

[fotuli index.html servido desde la VM]
