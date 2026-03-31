
# Trabajo Práctico N°2 — Informe de Experiencia

## Parte 1: Armado y verificación de cables Cat5/Cat5e (T568B Derecho)

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

Para la verificación utilizamos un **tester para cables ethernet**. El principio de funcionamiento es simple: el dispositivo envía señal por cada uno de los 8 pines y el extremo receptor indica con LEDs si la señal llega correctamente. Si los 8 LEDs se encienden en secuencia y en el orden correcto, el cable está bien construido.

**Resultado inicial:** el cable no pasó la verificación en el primer intento — debimos **rehacer el cable**. Tras revisar el crimpado y re-ordenar correctamente los conductores, repetimos la prueba y los **8 LEDs encendieron correctamente**, confirmando la continuidad eléctrica en todos los pares.

> Esta experiencia dejó en evidencia la importancia de verificar el orden exacto de los conductores antes de crimpar, ya que un error en ese paso obliga a rehacer todo el extremo.

---

### Intercambio y verificación entre grupos

Intercambiamos cables con otro grupo (Xi JinPing Revenge) y realizamos una inspección en dos etapas:

**a) Inspección visual**

Revisamos la calidad constructiva del cable recibido con criterio riguroso, evaluando:
- Alineación y orden correcto de los conductores dentro del conector RJ-45
- Longitud uniforme de los cables junto con la ficha
- Que la cubierta exterior del cable quedara sujeta por la lengüeta del conector
- Ausencia de conductores torcidos, cruzados o mal asentados

**Resultado:** el cable inspeccionado estaba correctamente armado. Nos pusimos extremadamente críticos pero no encontramos fallas significativas.

**b) Verificación eléctrica**

Realizamos también el test con el tester ethernet. Los 8 LEDs encendieron en secuencia correcta, confirmando continuidad en todos los pines.

---

