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
