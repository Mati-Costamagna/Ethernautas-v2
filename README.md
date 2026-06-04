# Trabajo Práctico N°5 — Server Survival

### Integrantes
- Costamagna, Matias Javier
- de la Mata, Nicolas
- Quispe, Mateo
- Sabena, Maria

### Objetivos
- Comprender cómo una arquitectura de servicios responde ante distintos tipos de tráfico.
- Relacionar componentes de infraestructura cloud con conceptos de redes: ruteo, balanceo de carga, almacenamiento, bases de datos, caché, colas y filtrado de tráfico malicioso.
- Analizar fallas, cuellos de botella y decisiones de escalabilidad.

---

## 1) Reconocimiento de arquitectura

Para cada componente respondemos brevemente:
- **a)** ¿Qué problema resuelve?
- **b)** ¿En qué capa(s) del modelo TCP/IP ubicamos su función principal?
- **c)** ¿Qué pasaría si ese componente falta en una arquitectura real?

| Componente | Problema que resuelve | Capa TCP/IP | Si falta... |
|---|---|---|---|
| **Firewall** | Filtra tráfico entrante y saliente según reglas de seguridad, bloqueando accesos no autorizados y tráfico malicioso | Capas 3 (Red) y 4 (Transporte) — filtra por IP, puerto y protocolo; los NGFW también operan en capa 7 (Aplicación) | El sistema queda expuesto a ataques directos (DDoS, escaneo de puertos, exploits). Todo el tráfico llega sin filtro a los servidores internos |
| **Load Balancer** | Distribuye las solicitudes entrantes entre múltiples instancias de un servicio para evitar sobrecargar un único nodo | Capa 4 (Transporte) — balanceo por TCP/UDP; o capa 7 (Aplicación) — balanceo por URL, headers HTTP | Un único servidor recibe todo el tráfico: se convierte en punto único de fallo y el sistema no puede escalar horizontalmente |
| **Queue** | Desacopla productores y consumidores de mensajes, absorbe picos de carga y garantiza el procesamiento ordenado de tareas | Capa 7 (Aplicación) — opera sobre protocolos de mensajería (AMQP, etc.) | Los productores deben esperar a que el consumidor procese cada solicitud; ante picos de tráfico el sistema se satura y pierde solicitudes |
| **Compute** | Ejecuta la lógica de la aplicación (servidores de aplicación, VMs, contenedores) que procesa las solicitudes de negocio | Capa 7 (Aplicación) — ejecuta la lógica de negocio sobre datos recibidos vía red | Sin cómputo no hay procesamiento: el sistema no puede responder a ninguna solicitud dinámica |
| **Serverless Function** | Ejecuta fragmentos de código bajo demanda sin gestionar infraestructura; ideal para tareas puntuales o de baja frecuencia | Capa 7 (Aplicación) — funciones invocadas por eventos HTTP, colas o timers | Las tareas puntuales deben ejecutarse en servidores siempre activos, aumentando costo y complejidad operativa |
| **SQL DB** | Almacena datos estructurados con soporte a transacciones ACID, relaciones y consultas complejas | Capa 7 (Aplicación) — acceso mediante protocolos propios (PostgreSQL wire protocol, MySQL protocol, etc.) | Sin persistencia relacional se pierden datos transaccionales o deben almacenarse en soluciones sin garantías de consistencia |
| **NoSQL** | Almacena datos semi-estructurados o no estructurados con alta escalabilidad horizontal y esquema flexible | Capa 7 (Aplicación) — acceso vía HTTP/REST (documentales) o protocolos propios | Las cargas con datos variables o de alto volumen no se ajustan bien a esquemas rígidos; se pierde flexibilidad y escalabilidad |
| **Cache** | Guarda en memoria resultados de consultas frecuentes para reducir latencia y la carga sobre la base de datos | Capa 7 (Aplicación) — actúa sobre respuestas de la capa de aplicación | Cada solicitud va directamente a la base de datos; aumentan la latencia y los costos de cómputo en cargas con muchas lecturas repetidas |
| **CDN** | Distribuye contenido estático desde nodos geográficamente cercanos al usuario, reduciendo latencia y tráfico al origen | Capas 3/4 (enrutamiento del request al nodo más cercano) y 7 (entrega del contenido HTTP/HTTPS) | Todo el contenido estático se sirve desde el servidor de origen: mayor latencia para usuarios lejanos y mayor ancho de banda consumido |
| **Storage** | Provee almacenamiento persistente de objetos o archivos (imágenes, videos, backups) desacoplado del cómputo | Capa 7 (Aplicación) — acceso vía APIs REST (S3, GCS, etc.) | Los archivos deben guardarse en el disco local del servidor de cómputo, lo que impide escalar horizontalmente y genera pérdida de datos ante fallos |
| **Search Engine** | Indexa grandes volúmenes de datos y permite búsquedas de texto completo con alta performance y relevancia | Capa 7 (Aplicación) — consultas vía API REST o protocolo propio | Las búsquedas recaen sobre la base de datos principal con consultas `LIKE`, lo que degrada el rendimiento y no ofrece ranking por relevancia |
| **Réplica** | Mantiene copias sincronizadas de la base de datos para distribuir la carga de lecturas y proveer tolerancia a fallos | Capa 7 (Aplicación) — replicación de datos vía protocolo propio del motor de base de datos | Toda lectura y escritura cae sobre el nodo primario; ante su fallo se pierde disponibilidad y no hay recuperación inmediata |

---

## 2) Tipos de tráfico

El simulador trabaja con: **STATIC, READ, WRITE, UPLOAD, SEARCH, MALICIOUS**.

| Tipo de tráfico | Ejemplo real | Componente recomendado | Riesgo si se procesa incorrectamente |
|---|---|---|---|
| **STATIC** | Imágenes, CSS o JS de una página web | CDN / almacenamiento estático | Desperdiciar capacidad de cómputo si lo sirve un servidor de aplicación |
| **READ** | | | |
| **WRITE** | | | |
| **UPLOAD** | | | |
| **SEARCH** | | | |
| **MALICIOUS** | | | |

---

## 3) Testeamos queues

Distribución de tráfico inicial usada:

| STATIC | READ | WRITE | UPLOAD | SEARCH | ATTACK |
|---|---|---|---|---|---|
| 30% | 20% | 15% | 5% | 10% | 20% |

**Observaciones:**

- **Al incrementar el rate, ¿qué sucede después de la queue?**

- **Manteniendo el rate alto y luego bajándolo a cero rápidamente, ¿qué sucede después de la queue?**

**Capturas:**
- `![Esquema queue](capturas/03-queue-esquema.png)`
- `![Rate alto](capturas/03-queue-rate-alto.png)`
- `![Drenado de la cola](capturas/03-queue-drenado.png)`

**Conclusión sobre el rol de la cola (desacople productor/consumidor, absorción de picos):**

---

## 4) Primera infraestructura mínima

La arquitectura debe intentar resolver: tráfico estático y uploads · lecturas y escrituras de datos · búsquedas · ataques / tráfico malicioso.

**Documentación con capturas:**

| Ítem | Captura | Notas |
|---|---|---|
| a) Arquitectura inicial | `![Arquitectura inicial](capturas/04-arquitectura.png)` | |
| b) Presupuesto inicial | `![Presupuesto](capturas/04-presupuesto.png)` | $___ |
| c) Estado de salud de los servicios | `![Salud](capturas/04-salud.png)` | |
| d) Momento en que empieza a fallar | `![Falla](capturas/04-falla.png)` | a los ___ min / ___ req/s |

**Preguntas:**

- **¿Qué componente falló primero?**

- **¿Por qué creés que falló?**

- **¿Fue un problema de capacidad, diseño, costo o seguridad?**

---

## 5) Escalabilidad y balanceo

Modificamos la arquitectura del punto 4 para soportar mayor tráfico. Probamos al menos **dos estrategias distintas** (opciones: más cómputo · balanceador de carga · caché · réplicas de lectura · cola de mensajes · separar servicios por tipo de tráfico).

### Estrategia 1: _(nombre)_
- **Cambio aplicado:** _(Completar)_
- **Resultado observado (evidencia del simulador):** _(req/s soportados, salud, presupuesto)_
- **Captura:** `![Estrategia 1](capturas/05-estrategia-1.png)`

### Estrategia 2: _(nombre)_
- **Cambio aplicado:** _(Completar)_
- **Resultado observado (evidencia del simulador):** _(Completar)_
- **Captura:** `![Estrategia 2](capturas/05-estrategia-2.png)`


- **¿Escalar horizontalmente siempre mejora el sistema? Justificá usando evidencia del simulador.**

---

## 6) Sobrevivir (modo Survival)

Diseñamos una arquitectura inicial sólida y tratamos de sobrevivir lo más posible mejorándola en modo **survival**.

**Arquitectura final (al momento del fallo):**
`![Arquitectura final](capturas/06-arquitectura-final.png)`

**Estadísticas finales:**

| Métrica | Valor |
|---|---|
| BUDGET final | $ |
| Upkeep Cost | -$ /s |
| Elapsed Time | min |
| Reputation | % |
| Load (RPS) | req/s |
| Failures (total) | |
| **TOTAL SCORE** | |

**Explicación:**

- **¿Por qué elegiste cada componente?**

- **¿Qué tráfico atiende cada uno?**

- **¿Qué cuello de botella apareció primero?**

- **¿Qué componente escalarías si tuvieras más presupuesto?**

---

## Conclusiones generales

