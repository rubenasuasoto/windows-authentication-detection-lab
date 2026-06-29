# Laboratorio de detección de autenticación de Windows

[English version](README.md)

Proyecto de portafolio seguro y reproducible con cinco detecciones Sigma sobre
anomalías de autenticación de Windows. El laboratorio valida la estructura de
las reglas, ejecuta escenarios sintéticos, convierte las reglas compatibles a
Splunk SPL y publica un informe bilingüe.

> Uso exclusivo en laboratorio defensivo. No contiene credenciales reales,
> registros de producción, malware, binarios, acceso a memoria ni simulaciones
> ofensivas.

## Qué demuestra

- Diseño de reglas y correlaciones Sigma.
- Pruebas positivas, negativas, de umbral y orientadas al ajuste.
- Tratamiento transparente de falsos positivos y limitaciones del backend.
- Validación e informes reproducibles mediante CI.
- Razonamiento alineado con ATT&CK sin ejecutar actividad sensible.

## Inicio rápido

Requiere Python 3.12 y [uv](https://docs.astral.sh/uv/).

```powershell
uv sync --extra dev
uv run authlab all
uv run pytest
```

El resultado visual se genera en `reports/latest/report.es.html`. Las consultas
Splunk y evidencias de ejecución se guardan en `artifacts/`, fuera del control de
versiones.

## Cómo revisar este proyecto

1. Empieza por `rules/manifest.json` y las cinco reglas Sigma de `rules/`.
2. Revisa `tests/fixtures/scenarios.json` para ver casos positivos, negativos,
   de umbral y de tuning.
3. Ejecuta `uv run authlab all` para regenerar validación, conversión SPL e
   informes.
4. Abre `reports/latest/report.es.html` para ver la matriz de validación.
5. Lee los playbooks por regla en `docs/playbooks/`.
6. Lee `docs/TUNING_GUIDE.md` para comprobar cómo se tratan falsos positivos
   sin ocultar el comportamiento detectado.

## Comandos

```text
authlab validate                 Valida reglas y ejecuta fixtures seguros
authlab convert --backend splunk Convierte reglas compatibles a Splunk SPL
authlab report                   Genera informes en inglés y español
authlab audit                    Rechaza artefactos privados o inseguros
authlab vm-check                 Comprueba la VM sin modificar Windows
authlab list-rules               Lista detecciones y playbooks enlazados
authlab explain AUTH-003         Explica una detección para revisión o entrevista
authlab all                      Ejecuta auditoría, validación, conversión e informes
```

El runner de fixtures es un oráculo educativo, no sustituye a un SIEM. Las
reglas conservan el estado `test` hasta validarse en un entorno autorizado.

## Siguiente fase

La [fase opcional de VM aislada](docs/VM_LAB.md) validará la telemetría real de
Windows mediante cuentas ficticias y acciones administrativas normales. No
incluye herramientas ofensivas ni datos de producción.

## Documentación técnica

- [Detection catalog](docs/DETECTION_CATALOG.md)
- [Per-rule playbooks](docs/playbooks/)
- [Validation and tuning](docs/VALIDATION.md)
- [Tuning guide](docs/TUNING_GUIDE.md)
- [Data sources](docs/DATA_SOURCES.md)
- [VM readiness checklist](docs/VM_READINESS_CHECKLIST.md)

## Presentación

La guía [Portfolio presentation guide](docs/PORTFOLIO_PRESENTATION.md) resume
cómo enseñar el proyecto en GitHub, LinkedIn o entrevistas sin exagerar su
alcance operativo.
