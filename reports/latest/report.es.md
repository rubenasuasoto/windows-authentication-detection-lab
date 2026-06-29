# Informe de validación

Laboratorio defensivo con eventos sintéticos. Este informe no acredita rendimiento en producción.

**Pack fingerprint:** `0eb0cb6cc201`

## Resumen

- Reglas válidas: 5/5
- Casos superados: 17/17
- Casos marcados para ajuste: 2
- Conversiones SPL correctas: 5/5

## Detecciones

| ID | Title | Events | Threshold | ATT&CK |
|---|---|---|---|---|
| AUTH-001 | Failed Logon Burst From One Source | 4625 | 5 events in 5 minutes per source and computer | T1110.001 |
| AUTH-002 | Failed Logons Across Multiple Accounts | 4625 | 4 distinct users in 10 minutes per source and computer | T1110.003 |
| AUTH-003 | Successful Logon After Repeated Failures | 4625, 4624 | 3 failures followed by success in 10 minutes for the same user and source | T1078 |
| AUTH-004 | Account Lockout Burst | 4740 | 3 lockouts in 15 minutes per caller and computer | Operational |
| AUTH-005 | Remote Logon Followed By Special Privileges | 4624, 4672 | Remote or network logon followed by privileges in 2 minutes for the same logon ID | T1078 |

## Matriz de validación

| Case | Rule | Category | Expected | Observed | Result | Disposition |
|---|---|---|---:|---:|---|---|
| AUTH-001-POS | AUTH-001 | positive | true | true | pass | keep |
| AUTH-001-NEG | AUTH-001 | negative | false | false | pass | keep |
| AUTH-001-BOUNDARY | AUTH-001 | boundary | false | false | pass | keep |
| AUTH-002-POS | AUTH-002 | positive | true | true | pass | keep |
| AUTH-002-NEG | AUTH-002 | negative | false | false | pass | keep |
| AUTH-002-BOUNDARY | AUTH-002 | boundary | false | false | pass | keep |
| AUTH-003-POS | AUTH-003 | positive | true | true | pass | keep |
| AUTH-003-NEG | AUTH-003 | negative | false | false | pass | keep |
| AUTH-003-BOUNDARY | AUTH-003 | boundary | false | false | pass | keep |
| AUTH-003-TUNE | AUTH-003 | false_positive | true | true | pass | tune |
| AUTH-004-POS | AUTH-004 | positive | true | true | pass | keep |
| AUTH-004-NEG | AUTH-004 | negative | false | false | pass | keep |
| AUTH-004-BOUNDARY | AUTH-004 | boundary | false | false | pass | keep |
| AUTH-005-POS | AUTH-005 | positive | true | true | pass | keep |
| AUTH-005-NEG | AUTH-005 | negative | false | false | pass | keep |
| AUTH-005-BOUNDARY | AUTH-005 | boundary | false | false | pass | keep |
| AUTH-005-TUNE | AUTH-005 | false_positive | true | true | pass | tune |

## Compatibilidad del backend

- **auth_001.yml**: native
- **auth_002.yml**: native
- **auth_003.yml**: native
- **auth_004.yml**: native
- **auth_005.yml**: native

## Notas de ajuste

- **AUTH-001**: Baseline trusted scanners and identity infrastructure before adding exclusions.
- **AUTH-002**: Review shared gateways and authorized identity-testing systems.
- **AUTH-003**: Compare with password resets, user mistakes and approved support activity.
- **AUTH-004**: Treat as an operational anomaly; investigate stale services and machine accounts first.
- **AUTH-005**: Baseline approved administration paths, jump hosts and service identities.

## Limitaciones

El runner es un oráculo educativo y no un SIEM. Las consultas generadas requieren revisión y pruebas autorizadas.
