# Laboratorio de detección de autenticación de Windows

[English version](README.md)

Laboratorio defensivo seguro y reproducible con cinco detecciones Sigma sobre
anomalías de autenticación de Windows. El laboratorio valida la estructura de
las reglas, ejecuta escenarios sintéticos, convierte las reglas compatibles a
Splunk SPL y publica un informe bilingüe.

> Uso exclusivo en laboratorio defensivo. No contiene credenciales reales,
> registros de producción, malware, binarios, acceso a memoria ni simulaciones
> ofensivas.

## Demo

Abre la demo publica guiada tipo mini-SOC:

https://rubenasuasoto.github.io/windows-authentication-detection-lab/reports/latest/demo.html

Lee la documentacion y los playbooks en GitBook:

https://2dam-7.gitbook.io/window-auth/

Abre la demo guiada tipo mini-SOC en local:

```powershell
uv run authlab demo --open
```

La demo es estatica y autocontenida. Usa solo datos sinteticos de laboratorio y
no sube archivos, no llama a un backend ni ingiere logs de produccion.

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
uv run authlab demo --open
uv run pytest
```

La demo guiada se genera en `reports/latest/demo.html` y el informe visual en
`reports/latest/report.es.html`. Las consultas Splunk y evidencias de ejecución
se guardan en `artifacts/`, fuera del control de versiones.

## Cómo revisar este proyecto

1. Abre la demo publica, o ejecuta `uv run authlab demo --open` en local, y
   recorre los casos sintéticos guiados.
2. Empieza por `rules/manifest.json` y las cinco reglas Sigma de `rules/`.
3. Revisa `tests/fixtures/scenarios.json` para ver casos positivos, negativos,
   de umbral y de tuning.
4. Ejecuta `uv run authlab all` para regenerar validación, conversión SPL e
   informes.
5. Abre `reports/latest/report.es.html` para ver la matriz de validación.
6. Lee los playbooks por regla en `docs/playbooks/`.
7. Revisa `docs/ALERT_NARRATIVES.md` para ver resumenes de alerta escritos como analista.
8. Lee `docs/TUNING_GUIDE.md` para comprobar cómo se tratan falsos positivos
   sin ocultar el comportamiento detectado.

Para una revision externa, el recorrido corto es: demo publica, `AUTH-003-POS`,
playbook en GitBook e informe de validacion.

## Comandos

```text
authlab validate                 Valida reglas y ejecuta fixtures seguros
authlab convert --backend splunk Convierte reglas compatibles a Splunk SPL
authlab report                   Genera informes en inglés y español
authlab demo                     Genera la demo local guiada tipo mini-SOC
authlab demo --open              Genera y abre la demo local
authlab audit                    Rechaza artefactos privados o inseguros
authlab vm-check                 Comprueba la VM sin modificar Windows
authlab vm-plan                  Imprime el plan opcional de validacion en VM
authlab list-rules               Lista detecciones y playbooks enlazados
authlab explain AUTH-003         Explica una detección para revisión o entrevista
authlab playbook AUTH-001        Imprime un playbook de deteccion
authlab narrative AUTH-001       Imprime una narrativa de alerta
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
- [Documentacion publica en GitBook](https://2dam-7.gitbook.io/window-auth/)
- [Documentacion preparada para GitBook](docs/README.md)
- [Guia de configuracion GitBook](docs/GITBOOK_SETUP.md)
- [Guia de configuracion GitBook en espanol](docs/GITBOOK_SETUP.es.md)
- [Alert narratives](docs/ALERT_NARRATIVES.md)
- [Per-rule playbooks](docs/playbooks/)
- [Validation and tuning](docs/VALIDATION.md)
- [Tuning guide](docs/TUNING_GUIDE.md)
- [Data sources](docs/DATA_SOURCES.md)
- [Release checklist](docs/RELEASE_CHECKLIST.md)
- [VM readiness checklist](docs/VM_READINESS_CHECKLIST.md)

## Presentación

La guía [Reviewer guide](docs/REVIEWER_GUIDE.md) resume cómo enseñar el
proyecto en una revisión técnica sin exagerar su alcance operativo.

## Release

La version `0.1.0` esta definida en `pyproject.toml`. Antes de crear el tag
publico, usa [docs/RELEASE_CHECKLIST.md](docs/RELEASE_CHECKLIST.md). El badge
de GitHub Actions, la demo publica y la documentacion GitBook ya estan
enlazados para revision externa.
