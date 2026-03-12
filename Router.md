### LAN Default Gateway
- MAC Address: AA:44:43
- IP: 10.6.0.1
- Subnet Mask: 255.255.0.0

### Concentrador
- MAC Address: AA:43:80

---

**Paquete 1:**

Recibido
- MAC Origen: AC:44:36
- MAC Destino: AA:44:43
- IP Origen: 10.6.0.103
- IP Destino: 10.2.0.103
- TTL 6

Enviado
- MAC Destino: AA:43:80
- MAC Origen: AA:44:43
- IP Origen: 10.6.0.103
- IP Destino: 10.2.0.103
- TTL 5

**PAQUETE ENVIADO AL CONCENTRADOR**

---

**Paquete 2:**

Recibido
-MAC destino: AA:44:43
-MAC origen: AB:44:86
-IP origen: 10.6.0.104
-IP destino: 10.4.0.102
-TTL: 6

Enviado
-MAC destino: AA:43:80
-MAC origen: AA:44:43
-IP origen: 10.6.0.104
-IP destino: 10.4.0.102
-TTL: 5

**PAQUETE ENVIADO AL CONCENTRADOR**

---

**Paquete 3:**

Recibido
-MAC destino: AA:44:43
-MAC origen: AA:43:12
-IP origen: 10.6.0.102
-IP destino: 10.6.0.104
-TTL: 6

Enviado
-MAC destino: AB:44:86
-MAC origen: AA:44:43
-IP origen: 10.6.0.102
-IP destino: 10.6.0.104
-TTL: 5

**PAQUETE ENVIADO AL HOST 4**

---

**Paquete 4:**

Recibido
- MAC destino: AA:44:43
- MAC origen: AA:43:80
- IP origen: 10.11.0.102
- IP destino: 10.6.0.105
- TTL 4

Enviado
**UNREACHABLE HOST**

---

**Paquete 5:**

Recibido
- MAC destino: AA:44:43
- MAC origen: AA:43:80
- IP origen: 10.9.0.101
- IP destino: 10.6.0.102
- TTL 4

Enviado
- MAC destino: AA:43:12
- MAC origen: AA:44:43
- IP origen: 10.9.0.101
- IP destino: 10.6.0.102
- TTL 3

**PAQUETE ENVIADO AL CONCENTRADOR**

---

**Paquete 6:**
Recibo
- MAC destino: AA:44:43
- MAC origen: AA:43:80
- IP origen: 10.10.0.101
- IP destino: 10.6.0.101
- TTL 3

Envio

**UNREACHABLE HOST**