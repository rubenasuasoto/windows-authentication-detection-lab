# Configuracion de GitBook

Usa GitBook como capa de documentacion visual para que una empresa pueda leer
los playbooks sin navegar por Markdown crudo en GitHub.

## Configuracion Recomendada

- Repositorio: `rubenasuasoto/windows-authentication-detection-lab`.
- Rama: `main`.
- URL publica: `https://2dam-7.gitbook.io/window-auth/`.
- Direccion inicial de sincronizacion: `GitHub -> GitBook`.
- Raiz de contenido: configurada por `.gitbook.yaml` como `./docs/`.
- Primera pagina: `README.md`.
- Tabla de contenidos: `SUMMARY.md`.

El repositorio ya incluye `.gitbook.yaml` en la raiz:

```yaml
root: ./docs/

structure:
  readme: README.md
  summary: SUMMARY.md
```

## Pasos En GitBook

1. Crea un Space nuevo en GitBook.
2. Abre la configuracion del Space y activa GitHub Sync.
3. Autoriza o instala la app de GitBook para este repositorio.
4. Selecciona `rubenasuasoto/windows-authentication-detection-lab`.
5. Selecciona la rama `main`.
6. Usa `GitHub -> GitBook` para la primera importacion.
7. Comprueba que la barra lateral usa `docs/SUMMARY.md`.
8. Abre la seccion Playbooks y verifica que cargan los cinco `AUTH-*`.
9. Publica el Space solo cuando todo renderice correctamente.

Playbooks esperados:

- `AUTH-001` failed logon burst.
- `AUTH-002` multiple accounts.
- `AUTH-003` success after failures.
- `AUTH-004` account lockout burst.
- `AUTH-005` privileged remote logon.

## Checks Antes De Compartir

- No subas logs de produccion, `.evtx`, capturas con datos privados,
  credenciales, tokens, binarios ni volcados de memoria.
- Mantén GitBook conectado al repositorio para evitar copias duplicadas.
- Comprueba que el aviso de laboratorio sintetico sigue visible.
- Manten la URL publica en el README solo mientras el Space siga publicado y
  verificado manualmente.

## Recorrido Para Empresa

1. Abre GitBook en la pagina Overview.
2. Entra en Playbooks.
3. Abre `AUTH-003 Successful logon after repeated failures`.
4. Enseña las preguntas de triaje, decision y tuning.
5. Vuelve a Validation para explicar la evidencia sintetica.
6. Termina en Portfolio presentation para enmarcar alcance y limitaciones.
