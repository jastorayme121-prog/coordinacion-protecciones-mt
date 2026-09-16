# Estudio de Coordinación de Protecciones de Sobrecorriente
## Alimentador Radial de Media Tensión — Caso de Estudio Genérico

---

## 1. Introducción

La coordinación de protecciones tiene como objetivo garantizar que, ante una
falla en cualquier punto del sistema, opere primero la protección más cercana
a la falla (protección primaria), y que la protección aguas arriba (respaldo)
solo actúe si la primaria falla en despejar la falla dentro de un tiempo
establecido.

Este estudio presenta un caso genérico de dos relés de sobrecorriente (51/50)
conectados en serie en un alimentador radial de 13.8 kV, y desarrolla la
metodología completa para calcular sus ajustes coordinados.

## 2. Descripción del sistema

```
   Subestación                                    Carga
   ┌─────────┐      Relé A         Relé B
   │  Barra   │───────[R-A]───────────[R-B]──────► Alimentador
   │  13.8 kV │      (respaldo)    (primario)
   └─────────┘
```

| Parámetro | Valor |
|---|---|
| Tensión nominal | 13.8 kV |
| Corriente de carga máxima (alimentador) | 250 A |
| Corriente de cortocircuito trifásica en barra de R-B | 3500 A |
| Relación de transformación TC (Relé A) | 400/5 |
| Relación de transformación TC (Relé B) | 300/5 |

## 3. Criterios de ajuste

### 3.1 Corriente de arranque (pickup)

El pickup se ajusta típicamente entre **1.25 y 1.5 veces la corriente máxima
de carga**, para evitar disparos por sobrecarga normal, pero garantizando
sensibilidad ante fallas.

- **Relé B (primario):** Ipickup = 1.3 × 250 A = 325 A → 325/300 = **1.08 × In (TC)**
- **Relé A (respaldo):** Ipickup = 1.3 × 250 A = 325 A → 325/400 = **0.81 × In (TC)**

### 3.2 Curva característica

Se utiliza la curva **IEC Normal Inversa (NI)**, definida por:

```
t(I) = TMS × [ 0.14 / ( (I/Ipickup)^0.02 − 1 ) ]
```

Donde:
- `t(I)`: tiempo de operación en segundos
- `I`: corriente de falla vista por el relé
- `Ipickup`: corriente de arranque ajustada
- `TMS`: dial de tiempo (Time Multiplier Setting)

### 3.3 Margen de coordinación (CTI)

Se adopta un **CTI (Coordination Time Interval) de 0.3 s**, valor típico
recomendado quwe cubre:
- Tiempo de apertura del interruptor aguas abajo (≈ 0.05–0.08 s)
- Sobrepaso del relé (overtravel) (≈ 0.05–0.1 s)
- Margen de seguridad (≈ 0.1–0.15 s)

## 4. Cálculo del TMS

**Paso 1 — Ajustar el relé primario (Relé B):**
Se selecciona un TMS bajo (respuesta rápida) que cumpla con los tiempos
mínimos de operación del fabricante. Para este caso: `TMS_B = 0.10`.

**Paso 2 — Calcular el tiempo de operación del Relé B ante la falla máxima:**
Con I_falla = 3500 A y Ipickup_B = 325 A → múltiplo = 10.77 × Ipickup

```
t_B = 0.10 × [0.14 / (10.77^0.02 − 1)] ≈ 0.28 s
```

**Paso 3 — Ajustar el Relé A (respaldo) para que opere 0.3 s después:**

```
t_A = t_B + CTI = 0.28 + 0.30 = 0.58 s
```

**Paso 4 — Despejar TMS_A** para esa corriente de falla (vista por Relé A,
mismo nivel de falla ya que está en serie) e Ipickup_A = 0.81 × In:

```
TMS_A = t_A / [0.14 / (múltiplo^0.02 − 1)] ≈ 0.21
```

## 5. Verificación de la coordinación

El script `src/tcc_curves.py` grafica ambas curvas TCC superpuestas y calcula
automáticamente el margen de coordinación (Δt) en el punto de falla máxima,
confirmando que se cumple el CTI mínimo de 0.3 s en todo el rango de corriente
de interés.

## 6. Conclusiones

- Los ajustes calculados garantizan selectividad entre el Relé A (respaldo) y
  el Relé B (primario) para fallas en el alimentador protegido por B.
- El margen de coordinación se mantiene por encima de 0.3 s en el rango de
  corrientes de falla analizado (desde el pickup hasta la falla máxima).
- Se recomienda validar estos ajustes con estudios de flujo de carga y
  cortocircuito actualizados, y revisarlos ante cualquier cambio en la
  topología del sistema o en la demanda del alimentador.

## 7. Referencias

- IEC 60255-151: Functional requirements for over/under current protection
- IEEE Std 242 (Buff Book): Protection and Coordination of Industrial and
  Commercial Power Systems
