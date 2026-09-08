# Despliegue en Streamlit Cloud

## Visión general

La aplicación está desplegada automáticamente en Streamlit Cloud y se actualiza con cada push a la rama `main` en GitHub.

**URL de la app:** https://humanity-last-exam-cx4xhpfjwl8s2s9s5fi55y.streamlit.app/

## Requisitos previos

- Repositorio público o privado en GitHub
- Cuenta en [Streamlit Community Cloud](https://streamlit.io/cloud)
- Variable de entorno `APP_PASSWORD` configurada en Streamlit Cloud (contraseña de acceso)

## Primer despliegue

### 1. Acceder a Streamlit Cloud

Ve a [share.streamlit.io](https://share.streamlit.io) y haz login con tu cuenta de GitHub.

### 2. Crear una nueva app

Haz click en **"New app"** (esquina superior derecha):

```
┌─────────────────────────────────────────────┐
│  [New app ▼]                                │
└─────────────────────────────────────────────┘
```

### 3. Seleccionar repositorio

- **Repository:** `Tuldor/humanity-last-exam`
- **Branch:** `main`
- **Main file path:** `streamlit_app.py`

### 4. Configurar secretos (importante ⚠️)

Después de crear la app:

1. Click en **"Advanced settings"** (abajo en la sección de configuración)
2. Click en **"Secrets"**
3. Pega tu contraseña en formato TOML:

```toml
app_password = "tu_contraseña_aquí"
```

4. Click en **"Save"**

**Nota:** Los secretos se guardan encriptados en Streamlit Cloud y no se versionan en git.

### 5. Esperar al despliegue

La app se compilará automáticamente. Esto toma 2-5 minutos la primera vez.

## Actualizaciones automáticas

Cada vez que hagas un push a `main` en GitHub:

```bash
git push origin main
```

Streamlit Cloud detecta el cambio automáticamente y redeploya la app (~1-2 minutos).

### Ver progreso del despliegue

En [share.streamlit.io](https://share.streamlit.io), haz click en tu app y verás un indicador de estado:

- 🔵 **Deploying** — Se está compilando
- 🟢 **Healthy** — Listo y funcionando
- 🔴 **Error** — Hay un problema (ver logs)

## Acceder a los logs

Si la app falla, puedes ver los errores:

1. Ve a [share.streamlit.io](https://share.streamlit.io)
2. Selecciona tu app
3. Click en el botón de menú (⋯) → **View logs**

Los logs muestran:
- Errores de Python
- Problemas de dependencias
- Mensajes de depuración

## Primera ejecución de usuarios

La primera vez que un usuario accede a la app:

1. **Pantalla de autenticación:** Debe ingresar la contraseña (`APP_PASSWORD`)
2. **Descarga del dataset:** Si es la primera ejecución del servidor, debe:
   - Aceptar términos en [huggingface.co/datasets/cais/hle](https://huggingface.co/datasets/cais/hle)
   - Generar un token en [huggingface.co/settings/tokens](https://huggingface.co/settings/tokens)
   - Pegarlo en la app
   - Esperar ~5-10 minutos a que descargue (~270 MB)

Después, el dataset se cachea en Streamlit Cloud y no se vuelve a descargar.

## Estructura de carpetas requerida

Para que Streamlit Cloud encuentre la app, la estructura debe ser:

```
humanity-last-exam/
├── streamlit_app.py          ← Punto de entrada (REQUERIDO)
├── src/
│   ├── app.py
│   └── i18n.py
├── data/
│   └── hle.parquet           ← Se descarga automáticamente
├── requirements.txt
├── .streamlit/
│   └── config.toml
└── wiki/
```

**Nota:** El archivo `streamlit_app.py` es esencial. Importa y ejecuta `src/app.py`.

## Variables de entorno

### APP_PASSWORD

Contraseña de acceso a la aplicación. Configurable en dos formas:

1. **Streamlit Secrets** (recomendado):
   ```toml
   # En Streamlit Cloud: Advanced settings → Secrets
   app_password = "mi_contraseña"
   ```

2. **Variable de entorno de sistema:**
   ```bash
   export APP_PASSWORD="mi_contraseña"
   ```

El código busca primero en secrets, luego en variables de entorno.

## Dependencias

Las dependencias están en `requirements.txt` y se instalan automáticamente:

```
streamlit>=1.56
datasets>=2.14.0
huggingface-hub>=0.17.0
pandas>=2.0
pillow>=10.0
pyarrow>=10.0
```

Para agregar nuevas dependencias:

1. Agrégalas a `requirements.txt`
2. Haz push a GitHub
3. Streamlit Cloud reinstalará automáticamente en el próximo despliegue

## Solución de problemas

### La app se queda en "Deploying"

- **Causa:** Dependencias faltantes o incompatibles en `requirements.txt`
- **Solución:** Revisa los logs. Asegúrate de que `requirements.txt` esté completo

### Error "APP_PASSWORD not found"

- **Causa:** El secreto no está configurado en Streamlit Cloud
- **Solución:** Ve a Advanced settings → Secrets y agrega `app_password = "..."`

### Dataset no se descarga (timeout)

- **Causa:** La descarga tarda más de lo permitido (Hugging Face está lento)
- **Solución:** Intenta de nuevo. El reintento automático eventualmente funcionará

### La app muestra código antiguo después de push

- **Causa:** Streamlit está usando caché local del navegador
- **Solución:** 
  - Limpia caché del navegador (Ctrl+Shift+Delete)
  - O fuerza recarga: Ctrl+Shift+R (Windows) o Cmd+Shift+R (Mac)

## Forzar redeploy manual

Si necesitas que Streamlit Cloud recompile aunque no hayas hecho cambios:

1. Ve a [share.streamlit.io](https://share.streamlit.io)
2. Busca tu app en la lista
3. Click en el menú (⋯) → **Rerun** o **Redeploy**

## Monitoreo

### Estado de la app

En el dashboard de Streamlit Cloud puedes ver:

- 📊 **CPU/RAM usage:** Consumo de recursos
- 👥 **Active users:** Usuarios conectados ahora
- 📈 **Total runs:** Número total de ejecuciones
- ⚠️ **Crashes:** Si la app ha crasheado recientemente

### Logs en tiempo real

En el panel de logs puedes ver:
- Accesos de usuarios
- Errores durante ejecución
- Mensajes de print/st.write

## Backups y recuperación

El dataset (`data/hle.parquet`) se descarga desde Hugging Face en la primera ejecución de cada servidor. No hay backups automáticos, pero el dataset siempre puede regenerarse.

Si necesitas recuperar versiones antiguas:

1. Revisa el historial de commits: `git log`
2. Haz revert a un commit anterior: `git revert <commit_hash>`
3. Haz push: `git push origin main`
4. Streamlit Cloud redeploya automáticamente
