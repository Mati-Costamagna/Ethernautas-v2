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

| Componente | a) Problema que resuelve | b) Capa TCP/IP | c) Si falta... |
|---|---|---|---|
| **Firewall** | | | |
| **Load Balancer** | | | |
| **Queue** | | | |
| **Compute** | | | |
| **Serverless Function** | | | |
| **SQL DB** | | | |
| **NoSQL** | | | |
| **Cache** | | | |
| **CDN** | | | |
| **Storage** | | | |
| **Search Engine** | | | |
| **Réplica** | | | |

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

Al incrementar el rate la queue mantiene la misma taza de salida sin importar el traffic rate de ingreso.

- **Manteniendo el rate alto y luego bajándolo a cero rápidamente, ¿qué sucede después de la queue?**

Sigue entregando los paquetes almacenados.

**Capturas:**
- `![Esquema queue](capturas/03-queue-esquema.png)`
- `![Rate alto](capturas/03-queue-rate-alto.png)`
- `![Drenado de la cola](capturas/03-queue-drenado.png)`

**Conclusión sobre el rol de la cola (desacople productor/consumidor, absorción de picos):**

La cola sirve para poder manejar el proceso de paquetes segun la velocidad con la que nuestro servicio puede procesarlos, permitiendonos seguir respondiendo con un trafico alto sin perjudicar nuestro servicio.

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

