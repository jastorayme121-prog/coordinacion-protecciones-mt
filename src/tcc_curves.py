"""
tcc_curves.py

Calcula y grafica las curvas Tiempo-Corriente (TCC) de dos relés de
sobrecorriente coordinados en serie, usando la curva IEC Normal Inversa.

Caso de estudio genérico: alimentador radial de media tensión con
Relé A (respaldo, aguas arriba) y Relé B (primario, aguas abajo).

Uso:
    python tcc_curves.py
"""

import numpy as np
import matplotlib.pyplot as plt
import os

# ---------------------------------------------------------------------------
# 1. Parámetros del sistema (datos de ejemplo, ver data/parametros_relés.csv)
# ---------------------------------------------------------------------------

# Corriente de falla trifásica máxima en el punto de coordinación (A)
I_FALLA_MAX = 3500.0

# Corriente de carga máxima del alimentador (A)
I_CARGA_MAX = 250.0

# Factor de pickup sobre la carga máxima
FACTOR_PICKUP = 1.3

# Margen de coordinación mínimo requerido (s)
CTI = 0.30

# Relaciones de transformación de los TC
RTC_A = 400 / 5
RTC_B = 300 / 5

# Pickup en A primarios
I_PICKUP_A = FACTOR_PICKUP * I_CARGA_MAX
I_PICKUP_B = FACTOR_PICKUP * I_CARGA_MAX

# Dial de tiempo (TMS) — Relé B ajustado primero (relé primario, rápido)
TMS_B = 0.10


# ---------------------------------------------------------------------------
# 2. Curva IEC Normal Inversa (NI)
# ---------------------------------------------------------------------------
def tiempo_operacion_ni(corriente, i_pickup, tms, k=0.14, alpha=0.02):
    """
    Calcula el tiempo de operación (s) de un relé con curva IEC Normal
    Inversa, para corrientes por encima del pickup.

    t(I) = TMS * [ k / ( (I/Ipickup)^alpha - 1 ) ]
    """
    multiplo = np.asarray(corriente, dtype=float) / i_pickup
    # Evitar división por cero / valores no operativos por debajo del pickup
    multiplo = np.where(multiplo > 1.001, multiplo, np.nan)
    return tms * (k / (multiplo**alpha - 1))


def calcular_tms_respaldo(i_falla, i_pickup, t_objetivo, k=0.14, alpha=0.02):
    """
    Despeja el TMS necesario para que el relé de respaldo opere en
    t_objetivo segundos ante la corriente de falla i_falla.
    """
    multiplo = i_falla / i_pickup
    return t_objetivo / (k / (multiplo**alpha - 1))


# ---------------------------------------------------------------------------
# 3. Cálculo de coordinación
# ---------------------------------------------------------------------------
def main():
    # Tiempo de operación del relé primario (B) ante la falla máxima
    t_B = tiempo_operacion_ni(I_FALLA_MAX, I_PICKUP_B, TMS_B)

    # Tiempo objetivo del relé de respaldo (A) = t_B + CTI
    t_A_objetivo = t_B + CTI

    # TMS del relé A para lograr ese tiempo ante la misma falla
    TMS_A = calcular_tms_respaldo(I_FALLA_MAX, I_PICKUP_A, t_A_objetivo)

    print("=== Resultados de coordinación ===")
    print(f"Pickup Relé A (respaldo): {I_PICKUP_A:.1f} A")
    print(f"Pickup Relé B (primario): {I_PICKUP_B:.1f} A")
    print(f"TMS Relé B (primario):    {TMS_B:.3f}")
    print(f"TMS Relé A (respaldo):    {TMS_A:.3f}")
    print(f"t operación Relé B @Ifalla_max: {t_B:.3f} s")
    print(f"t operación Relé A @Ifalla_max: {t_A_objetivo:.3f} s")
    print(f"Margen de coordinación (CTI):   {t_A_objetivo - t_B:.3f} s")

    # -----------------------------------------------------------------
    # 4. Graficar curvas TCC
    # -----------------------------------------------------------------
    corrientes = np.logspace(np.log10(I_PICKUP_B * 1.01), np.log10(I_FALLA_MAX * 1.3), 500)

    t_curva_B = tiempo_operacion_ni(corrientes, I_PICKUP_B, TMS_B)
    t_curva_A = tiempo_operacion_ni(corrientes, I_PICKUP_A, TMS_A)

    fig, ax = plt.subplots(figsize=(8, 6))
    ax.loglog(corrientes, t_curva_B, label="Relé B (primario)", linewidth=2)
    ax.loglog(corrientes, t_curva_A, label="Relé A (respaldo)", linewidth=2)

    ax.axvline(I_FALLA_MAX, color="gray", linestyle="--", linewidth=1,
               label=f"Falla máxima = {I_FALLA_MAX:.0f} A")
    ax.plot(I_FALLA_MAX, t_B, "o", color="C0")
    ax.plot(I_FALLA_MAX, t_A_objetivo, "o", color="C1")

    ax.set_xlabel("Corriente (A, primarios)")
    ax.set_ylabel("Tiempo de operación (s)")
    ax.set_title("Coordinación de protecciones — Curvas TCC (IEC Normal Inversa)")
    ax.grid(True, which="both", linestyle=":", linewidth=0.5)
    ax.legend()

    os.makedirs("resultados", exist_ok=True)
    output_path = os.path.join("resultados", "curvas_tcc.png")
    fig.savefig(output_path, dpi=150, bbox_inches="tight")
    print(f"\nGráfica guardada en: {output_path}")


if __name__ == "__main__":
    main()
