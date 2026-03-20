# TP N1

### Integrantes
- Costamagna, Matias Javier
- de la Mata, Nicolas
- Quispe, Mateo
- Sabena, Maria Pilar

---
# Parte 1 - Repaso general didáctico: Simulación de envío de paquetes, ARP y ruteo entre redes.

1) Las configuraciones realizadas por los integrantes se encuentran en los archivos `Parte_1/Host2.md`, `Parte_1/Host3.md`, `Parte_1/Host4.md`, `Parte_1/Router.md`.
Cada uno de estos archivos contiene las tarjetas NIC correspondientes y los paquetes que hayan sido enviados/recibidos por cada dispositivo de nuestra LAN.

---

2) La topologia de la red WAN contiene las direcciones de nuestra red LAN obtenidas a partir del protocolo ARP (tabla en `Parte_1/Routing_Table.md`)![Texto Alternativo](./Parte_1/Topologia.png)

---
5)

- a)    La dirección IP destino se mantiene constante durante todo el recorrido porque pertenece a la capa de red y tiene alcance extremo a extremo: identifica al destinatario final del paquete y no es modificado por los routers intermedios durante el enrutamiento.
La dirección MAC, en cambio, pertenece a la capa de enlace de datos y tiene alcance estrictamente local: solo es válida entre dos nodos directamente conectados. En cada salto, el router realiza un proceso de desencapsulación y reencapsulación: descarta la trama entrante (y con ella la MAC origen/destino del segmento anterior), consulta su tabla de ruteo usando la IP destino, y construye una nueva trama con las MACs correspondientes al siguiente tramo, obtenidas mediante el protocolo ARP.
Esto evidencia una separación fundamental: el direccionamiento IP resuelve a dónde debe llegar el paquete en la red global, mientras que el direccionamiento MAC resuelve cómo entregarlo en cada segmento local.

- b)  Cuando un host quiere enviar un paquete a otra red, no intenta descubrir la MAC del destino final sino la del default gateway, porque ARP opera mediante broadcasts y los routers no los reenvían, por lo que la consulta nunca cruzaría hacia la red remota. El host entonces usa ARP dentro de su LAN para obtener la MAC del gateway, construyendo la trama con esa MAC como destino pero manteniendo la IP final del host remoto sin modificar.
El gateway resuelve el impedimento de que el host está limitado a su segmento local en capa 2 y no tiene mecanismo para entregar tramas fuera de él. El gateway, al operar en la capa de red, interconecta redes distintas superando ese límite.

- c)  La principal ventaja del modelo hop-by-hop es que cada router solo necesita conocer el siguiente salto hacia el destino, no el camino completo. Esto lo hace escalable: agregar nuevos nodos o redes no requiere que todos los routers actualicen una visión global de la topología.
Al distribuir la decisión de encaminamiento entre todos los nodos, se elimina también el punto único de fallo que tendría un esquema centralizado. Si un enlace o router falla, los nodos vecinos detectan el cambio y redirigen el tráfico por rutas alternativas, sin intervención del host origen. El mismo mecanismo permite adaptarse a la congestión: los routers ajustan sus decisiones según las condiciones actuales de la red.

- d) El frame Ethernet contiene direcciones MAC que solo tienen sentido dentro de un mismo segmento de red, el frame ya cumplio su funcion de transporte dentro de la red asi que el router lo descarta y arma uno nuevo con las MACs correctas para el siguiente enlance. Si en cambio el router reenviara el mismo frame sin modificarlo, el siguiente dispositivo recibira un frame con una MAC destino que no le corresponde y lo descartaria.

- e) El TTL previene que los paquetes queden circulando indefinidamente en la red sin alcanzar nignun host, como esto le puede pasar a muchos paquetes a la vez, los enlaces y routers se podrian saturar procesando tráfico inútil hasta colapsar.

---
# Parte 2 — Inyección y detección de errores (EDAC)

Para realizar la actividad dividimos el aula en grupos de dos, donde cada grupo actuaba como host emisor y receptor al mismo tiempo. Los routers intermedios (otros grupos) podían modificar uno o más bits de la payload antes de reenviarla, sin avisarle al receptor. La idea era que cada grupo implementara su propia técnica de detección de errores y pudiera determinar de forma independiente si el paquete llegó tal como fue enviado, o si alguien le metió mano en el camino.

### Técnica EDAC utilizada

En nuestro caso usamos dos técnicas combinadas: **XOR al enviar** y **bit de paridad al recibir**.

---

### Al enviar — XOR por nibbles

Tomamos la payload de 16 bits, la dividimos en 4 grupos de 4 bits (nibbles) y les aplicamos XOR de forma sucesiva. El resultado es un checksum de 4 bits que mandamos junto con el paquete para que el receptor pueda verificarlo.

El XOR funciona así: dos bits iguales dan 0, dos bits distintos dan 1.

### Al recibir — Bit de paridad por nibble

Al recibir un paquete, calculamos el bit de paridad de cada nibble de la payload:
- Si la cantidad de `1`s en ese nibble es **par** → paridad `0`
- Si la cantidad de `1`s en ese nibble es **impar** → paridad `1`

Eso nos da 4 bits que comparamos con el EDAC que vino en el paquete. Si coinciden, el paquete está bien. Si no, alguien lo tocó.

---

## Paquetes

### Paquete 1 / Enviado

- **IP origen:** 10.0.2.0
- **IP destino:** 10.0.4.0
- **Payload:** e420 | `1110 0100 0010 0000`
- **EDAC:** 8 | `1000`

El EDAC lo calculamos hsiaciendo XOR entre los cuatro nibbles de la payload:

```
1110 XOR 0100 = 1010
1010 XOR 0010 = 1000
1000 XOR 0000 = 1000  ←  EDAC final
```

Ese `1000` (hex `8`) lo mandamos junto al paquete para que el receptor pudiera verificarlo.

---

### Paquete 2 / Recibido

- **IP origen:** 10.0.5.0
- **IP destino:** 10.0.2.0
- **Payload:** a9b1 | `1010 1001 1011 0001`
- **EDAC:** 3 | `0011`
- **Paquete no corrupto**

Para verificar, calculamos el bit de paridad de cada nibble de la payload recibida:

- `1010` → dos `1`s → par → `0`
- `1001` → dos `1`s → par → `0`
- `1011` → tres `1`s → impar → `1`
- `0001` → un `1` → impar → `1`

Paridad calculada: `0011`. Coincide exactamente con el EDAC recibido (`0011`), así que el paquete llegó sin modificaciones.

---
## Conclusión

La combinación de XOR en el emisor y paridad en el receptor nos permitió verificar la integridad del paquete recibido. En este caso, el paquete de `10.0.5.0` llegó íntegro.

Vale aclarar que estas técnicas son solo de **detección**, no de corrección: podemos saber que algo fue modificado, pero no recuperar la información original. Además, hay casos donde dos errores se cancelan entre sí y no los detectamos, que es una limitación conocida de estos métodos.
