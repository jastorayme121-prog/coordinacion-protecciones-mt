# Estudio de Coordinación de Protecciones - Alimentador Radial MT

Proyecto educativo que documenta la metodología y herramientas para realizar un
**estudio de coordinación de protecciones de sobrecorriente** en un alimentador
radial de media tensión (MT), utilizando relés con funciones 50/51 (ANSI) y
curvas de tiempo inverso según norma IEC 60255.

> ⚠️ Este repositorio usa **datos de ejemplo genéricos** con fines educativos y
> de demostración. No corresponde a ninguna instalación, cliente o empresa real.

## ¿Qué contiene este repositorio?

| Carpeta | Contenido |
|---|---|
| `docs/` | Estudio técnico completo (metodología, criterios, resultados) |
| `src/` | Script en Python para calcular y graficar curvas TCC (tiempo-corriente) |
| `data/` | Datos de ejemplo: parámetros de relés y del sistema |
| `resultados/` | Gráficas generadas por el script |

## Objetivo del estudio

Determinar los ajustes de corriente (pickup) y dial de tiempo (TMS) de dos
relés de sobrecorriente ubicados en serie en un alimentador radial, de forma
que se cumpla:

1. **Selectividad**: ante una falla aguas abajo, opera primero el relé más
   cercano a la falla.
2. **Margen de coordinación (CTI)**: se respeta un intervalo mínimo de tiempo
   (típicamente 0.2 - 0.4 s) entre la operación del relé principal y el de
   respaldo.
3. **Sensibilidad**: los relés detectan fallas mínimas dentro de su zona de
   protección.
4. **Rapidez**: se minimiza el tiempo de despeje de falla sin sacrificar
   selectividad.

## Cómo usar el script

```bash
pip install numpy matplotlib
python src/tcc_curves.py
```

Esto genera la gráfica de coordinación en `resultados/curvas_tcc.png`, mostrando
las curvas de ambos relés superpuestas y el margen de coordinación resultante.

## Metodología

Ver el estudio completo en [`docs/estudio_coordinacion.md`](docs/estudio_coordinacion.md).

## Autor

Estudio elaborado con fines educativos como parte de portafolio técnico en
ingeniería eléctrica / protecciones de sistemas de potencia.

## Licencia

MIT — libre uso educativo y de referencia.
