# Arquitectura de Protocolos y TCP/IP

Basado en *Comunicaciones y Redes de Computadores* (7ª edición) de William Stallings.

---

## Primera Parte: Cuestiones de Repaso

**2.1 ¿Cuál es la función principal de la capa de acceso a la red?**

    La función principal de la capa de acceso a la red es el intercambio de datos entre el sistema final (como una computadora o servidor) y la red a la que está conectado. Se encarga de aislar a las capas superiores de las especificidades del hardware, gestionando el direccionamiento físico (como las direcciones MAC), el enrutamiento de los datos dentro de la misma red física o enlace directo, y el control de acceso al medio de transmisión.

**2.2. ¿Qué tareas realiza la capa de transporte?**

    La capa de transporte tiene como propósito proporcionar un servicio de transferencia de datos de extremo a extremo entre los procesos de aplicación que se ejecutan en diferentes sistemas. Sus tareas principales incluyen:
    * Asegurar que los datos lleguen de forma confiable, ordenada y sin errores al proceso correcto (si utiliza TCP).
    * Segmentar los datos provenientes de la capa de aplicación en tamaños manejables antes de enviarlos a la capa de red, y reensamblarlos en el destino.
    * Proporcionar mecanismos de control de flujo y control de congestión.
    * Distinguir las distintas aplicaciones simultáneas que se ejecutan en un host mediante el uso de Puntos de Acceso al Servicio (SAP).

**2.3. ¿Qué es un protocolo?**

    Un protocolo es un conjunto formal de reglas y convenciones que gobiernan el formato y el intercambio de mensajes entre dos o más entidades de comunicación. Un protocolo define la sintaxis (formato y estructuración de los datos), la semántica (significado de la información de control para la coordinación y el manejo de errores) y la temporización (adaptación de velocidad y secuenciación de los datos).

**2.4. ¿Qué es una unidad de datos del protocolo (PDU)?**

    Una PDU (Protocol Data Unit) es un bloque de información que se intercambia entre entidades pares en una arquitectura de protocolos. Cada capa toma los datos de la capa superior y les añade su propia información de control específica (header). El conjunto de los datos de usuario encapsulados más la información de control de esa capa específica conforma la PDU (por ejemplo, el segmento en la capa de transporte, el datagrama en la capa de red, y la trama en la capa de acceso a la red).

**2.5. ¿Qué es una arquitectura de protocolos?**

    Una arquitectura de protocolos es la estructura de software y hardware que divide la compleja tarea de las comunicaciones en un conjunto de módulos o "capas" independientes y jerárquicas. Cada capa se encarga de un subconjunto específico de funciones y ofrece sus servicios a la capa inmediatamente superior, apoyándose en los servicios que le proporciona la capa inferior.

**2.6. ¿Qué es TCP/IP?**

    TCP/IP (Transmission Control Protocol/Internet Protocol) es la arquitectura de protocolos estándar más utilizada en el mundo, base de las comunicaciones en Internet. Es un modelo estructurado en capas (Aplicación, Transporte, Internet y Acceso a la Red) que permite el intercambio de datos entre dispositivos de múltiples fabricantes, facilitando la interconexión de redes heterogéneas.

**2.7. ¿Qué ventajas aporta una arquitectura en capas como la usada en TCP/IP?**

    * Modularidad e independencia: Los cambios en la tecnología de una capa específica no requieren reescribir el software de las demás capas, siempre y cuando se mantengan las interfaces.
    * Facilidad de diseño e implementación: Reduce la complejidad del desarrollo, ya que los ingenieros pueden enfocarse en una sola capa a la vez.
    * Estandarización: Facilita la interoperabilidad entre fabricantes distintos.

**2.8. ¿Qué es un encaminador?**

    Un encaminador (router) es un dispositivo de interconexión de redes que opera en la capa de red (Capa de Internet en TCP/IP). Su tarea principal es conectar redes distintas y determinar la ruta óptima por la cual deben viajar los paquetes de datos desde su origen hasta su destino final, basándose en direcciones IP y protocolos de enrutamiento.

---

## Segunda Parte: Ejercicios

**2.1. Procedimiento de pedir y enviar una pizza (Modelo de Capas)**

    Podemos definir tres niveles principales para ilustrar este proceso:
    * Capa 3 (Aplicación): El Cliente hambriento y el Cocinero. Interacción lógica: El cliente quiere una pizza y el cocinero hace una pizza para él. El mensaje del cliente ("quiero una pizza") llega lógicamente al cocinero, y el producto llega al cliente.
    * Capa 2 (Comunicación/Enlace): El Teléfono del cliente y el Recepcionista. Interacción: Esta capa traduce el "deseo" en un pedido formal. El teléfono establece la conexión y transmite el mensaje hablado; el recepcionista toma la orden y se la pasa a la Capa 3 (el cocinero).
    * Capa 1 (Física/Red): El Repartidor y las Calles. Interacción: La pizza terminada (PDU de la capa superior) se "encapsula" en una caja. El repartidor usa un medio físico (la calle) para llevarla a la dirección de destino y entregarla.

**2.2. Diagramas de comunicación con traductores**

**a) Primeros Ministros con traductores al inglés**
![Diagrama 2.2.a)](./Diagramas/)

b) Inclusión de un traductor intermedio en Alemania (Nudo de Red / Router)
Alemania actúa como un nodo intermedio operando hasta la Capa 2 para enrutar/traducir y volver a bajar a la Capa 1.
![Diagrama 2.2.a)](./Diagramas/)

**2.3. Enumere las desventajas del diseño en capas para los protocolos.**

    - Sobrecarga (Overhead): Cada capa añade su propia cabecera a los datos. En mensajes pequeños, las cabeceras pueden pesar más que los datos útiles.
    - Duplicación de funciones: Diferentes capas pueden realizar tareas redundantes (ej. control de errores en la capa de enlace y en la de transporte).
    - Procesamiento adicional: Subir y bajar por las capas consume CPU y memoria, introduciendo latencia.
    - Ocultación de información: El aislamiento estricto impide que capas superiores usen información valiosa de capas inferiores para optimizar el rendimiento.

**2.4. El problema de los dos ejércitos azules**
* Deteccion de errores.
    Respuesta: Matemáticamente, no existe ningún protocolo que pueda garantizar el éxito al 100% utilizando un canal no fiable. Si un general envía un mensaje, necesita confirmación. Si el otro envía la confirmación, ahora él necesita una confirmación de que su confirmación llegó, creando un bucle infinito de incertidumbre. En la práctica (como en TCP), no se busca la certeza matemática absoluta, sino una probabilidad de éxito suficientemente alta utilizando temporizadores y retransmisiones.

**2.5. ¿Es necesaria o no una capa de red en una red de difusión?**

    En una red de difusión pura y aislada (como una LAN local en bus donde todos los equipos "se escuchan" directamente), la capa de red no es estrictamente necesaria. La subcapa MAC (Capa 2) ya se encarga de direccionar físicamente las tramas al destinatario correcto dentro de ese medio compartido. Sin embargo, la capa de red se vuelve imprescindible tan pronto como se necesite interconectar esa LAN con otras redes diferentes (como Internet), ya que proporciona el enrutamiento lógico jerárquico.

**2.6. Diseño de arquitecturas basadas en los principios de la Tabla 2.1**

    a) Arquitectura de 8 capas: Se podría añadir una "Capa de Seguridad de Datos" entre la Presentación y la Aplicación. Ejemplo: Una red bancaria, donde esta capa se encarga del cifrado asimétrico y la firma digital antes de que la aplicación procese los montos.

    b) Arquitectura de 6 capas: Se podrían fusionar la Capa de Sesión y la Capa de Presentación en una sola "Capa de Diálogo y Formato". Ejemplo: Redes de sensores IoT o streaming de video, donde el control de la sesión y la codificación de datos están tan entrelazados que separarlos sólo añade sobrecarga innecesaria.

**2.7. Encapsulación, segmentación y agrupamiento**

    a) Segmentación: ¿Es necesario que cada segmento del nivel (N-1) contenga una copia de la cabecera del nivel N? No. La capa N-1 trata a toda la PDU de nivel N (datos + cabecera N) como un solo bloque de datos a dividir. La cabecera N original quedará dentro del primer fragmento. Lo que sí hace la capa N-1 es añadir su propia cabecera N-1 a cada fragmento para poder reensamblarlos.

    b) Agrupamiento: ¿Es necesario que cada PDU conserve su cabecera? Sí. Cuando la capa N-1 agrupa varios mensajes pequeños de la capa N en una sola PDU N-1 de transmisión, cada PDU original de nivel N debe conservar su propia cabecera. De lo contrario, cuando el paquete llegue al destino y se desempaquete, la capa N destino no sabría cómo distinguir o procesar cada mensaje individual.