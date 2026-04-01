# TP N2

### Integrantes
- Costamagna, Matias Javier
- de la Mata, Nicolas
- Quispe, Mateo
- Sabena, Maria Pilar

---
## Parte 1: Armado y verificación de cables Cat5/Cat5e bajo estándar T568A/B

### Construcción del cable

Armamos un cable UTP Cat5e bajo la norma **T568B**, del tipo **derecho (no cruzado)**, de aproximadamente 1 metro de longitud. El orden de los conductores fue:

| Pin | Color         |
|-----|---------------|
| 1   | Blanco-Naranja |
| 2   | Naranja        |
| 3   | Blanco-Verde   |
| 4   | Azul           |
| 5   | Blanco-Azul    |
| 6   | Verde          |
| 7   | Blanco-Marrón  |
| 8   | Marrón         |

### Verificación eléctrica

Para la verificación utilizamos un tester para cables Ethernet. El principio de funcionamiento es simple: el dispositivo envía señal por cada uno de los 8 pines y el extremo receptor indica con LEDs si la señal llega correctamente. Si los 8 LEDs se encienden en secuencia y en el orden correcto, el cable está bien construido.

**Resultado inicial:** el cable no pasó la verificación en el primer intento, por lo que debimos rehacerlo. Tras revisar el crimpado y reordenar correctamente los conductores, repetimos la prueba y los 8 LEDs encendieron correctamente, confirmando la continuidad eléctrica en todos los pares.

Esta experiencia dejó en evidencia la importancia de verificar el orden exacto de los conductores antes de crimpar, ya que un error en ese paso obliga a rehacer todo el extremo del cable.

---

### Intercambio y verificación entre grupos

Intercambiamos cables con otro grupo ("Xi JinPing Revenge") y realizamos una inspección en dos etapas:

**a) Inspección visual para la calidad constructiva **

Revisamos la calidad constructiva del cable recibido con criterio riguroso, evaluando:
- Alineación y orden correcto de los conductores dentro del conector RJ-45
- Longitud uniforme de los cables junto con la ficha
- Que la cubierta exterior del cable quedara sujeta por la lengüeta del conector
- Ausencia de conductores torcidos, cruzados o mal asentados

<img src="./Parte_1/assets/Cable UTP Xi JinPing Revenge.jpeg" alt="Switch TL-SF1008D" width="300">

**[Extremo de cable del grupo Xi JingPing Revenge]**

<img src="./Parte_1/assets/Verificacion visual 1.jpeg" alt="Switch TL-SF1008D" width="300">

**[Inspección crítica - Parte 1]**

<img src="./Parte_1/assets/Verificacion visual 2.jpeg" alt="Switch TL-SF1008D" width="300">

**[Inspección crítica - Parte 2]**

<img src="./Parte_1/assets/Verificacion visual 3.jpeg" alt="Switch TL-SF1008D" width="300">

**[Inspección crítica - Parte 3]**

**Resultado:** El cable inspeccionado estaba correctamente armado. El único detalle encontrado fue que el conductor **Verde** no alcanzaba visualmente el fondo del conector.

**b) Verificación eléctrica utilizando un tester**

Realizamos el test correspondiente con el tester Ethernet. Los 8 LEDs encendieron en la secuencia correcta, confirmando la continuidad en todos los cables; a pesar de notar visualmente que el conductor **Verde** no llegaba al fondo, este hacía el contacto suficiente con los pines metálicos del conector RJ-45.

<img src="./Parte_1/assets/Verificacion en proceso.jpeg" alt="Switch TL-SF1008D" width="300">

**[Verificación eléctrica en proceso]**

<img src="./Parte_1/assets/Verificacion aprobada.jpeg" alt="Switch TL-SF1008D" width="300">

**[Verificación eléctrica aprobada]**

---

## Parte 2: Equipamiento físico, verificación y utilización de equipos de red y análisis de tráfico.

1)  En nuestro caso no pudimos realizar la conexión de consola con el switch Cisco Catalyst 2950 Series, por lo que utilizamos un equipo alternativo disponible en el laboratorio para realizar las pruebas de red local.

**TP-Link TL-SF1008D — Switch de 8 puertos 10/100 Mbps**

<img src="./Parte_2/assets/switch.jpg" alt="Switch TL-SF1008D" width="300">

**Características principales del switch**

| Característica             | Detalle                                      |
|---------------------------|----------------------------------------------|
| Estándares                | IEEE 802.3, IEEE[Extremo de cable del grupo Xi JingPing Revenge] 802.3u, IEEE 802.3x, CSMA/CD |
| Puertos                   | 8 x RJ45 10/100 Mbps, Auto-Negociación, Auto-MDI/MDIX |
| Tasa de transferencia     | 10/100 Mbps (Half Duplex) / 20/200 Mbps (Full Duplex) |
| Control de flujo       | IEEE 802.3x (Full Duplex) / Back-Pressure (Half Duplex) |
| Método de transmisión  | Store-and-Forward                                        |

2) Al no contar con suficiente tiempo, ni con los adaptadores USB-Serie y cables necesarios para la configuración de consola , el grupo "The Lord of Pings" se encargó de intentar acceder a la administración del switch Cisco. Nuestro grupo se dedicó íntegramente a establecer la conexión física y lógica utilizando el switch TP-Link.

3) ara verificar la conectividad, conectamos nuestra computadora al switch utilizando los cables armados en la Parte 1. Una vez establecida la conexión física, procedimos a realizar un ping hacia la PC de otro grupo.

Durante esta etapa nos encontramos con un problema de enrutamiento: inicialmente, ambos dispositivos (con sistema operativo Linux) no lograban comunicarse mediante asignación manual de IP, obteniendo como respuesta **Unreachable host**. La solución consistió en utilizar un dispositivo con sistema operativo Windows en uno de los extremos. Al no existir un servidor DHCP en la red, Windows utilizó su protocolo APIPA (Automatic Private IP Addressing) para autoconfigurarse una dirección en el rango 169.254.x.x. Conociendo esta dirección, pudimos realizar el ping exitosamente desde el otro equipo.

<img src="./Parte_2/assets/Conexion con Switch.jpeg" alt="Switch TL-SF1008D" width="300">

**[Configuración de red utilizada para las pruebas de conectividad]**

**Resultado:**

```
Pinging 169.254.105.129 with 32 bytes of data:
Reply from 169.254.105.129: bytes=32 time=1ms TTL=64
Reply from 169.254.105.129: bytes=32 time=1ms TTL=64
Reply from 169.254.105.129: bytes=32 time=1ms TTL=64
Reply from 169.254.105.129: bytes=32 time=1ms TTL=64

Ping statistics for 169.254.105.129:
    Packets: Sent = 4, Received = 4, Lost = 0 (0% loss),
Approximate round trip times in milli-seconds:
    Minimum = 1ms, Maximum = 1ms, Average = 1ms
```

**Análisis:**
- **4 paquetes enviados, 4 recibidos, 0% de pérdida** → conectividad perfecta.
- **Latencia de 1ms** → tiempo de respuesta mínimo, esperado en una red local LAN cableada.
- **TTL de 64** → Indica que los paquetes llegaron directamente en Capa 2 a través del switch, sin atravesar ningún router que decremente el "Time To Live".

---
## Conclusión

El desarrollo de este trabajo práctico nos permitió tomar contacto directo con los elementos de la capa física y ganar experiencia real en el armado y verificación de conexiones de red. Durante la primera etapa, comprobamos que la precisión constructiva es vital; un pequeño error en la alineación de los pares al crimpar un cable obliga a reiniciar el proceso, destacando la utilidad de las herramientas de verificación visual y eléctrica.

En la segunda etapa, aunque nos enfrentamos a limitaciones de hardware para acceder a la configuración por consola del equipo Cisco, logramos sortear el obstáculo de conectividad lógica comprendiendo cómo interactúan los sistemas operativos ante la ausencia de un servidor DHCP. El uso de una dirección APIPA nos facilitó establecer una red funcional en Capa 2 y verificar la comunicación integral de extremo a extremo mediante el envío de paquetes ICMP. En conjunto, la experiencia unificó la teoría con la resolución de problemas prácticos que son habituales en el despliegue de redes físicas.