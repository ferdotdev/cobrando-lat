<div align="center">
  <div style="display: inline-flex; align-items: center; gap: 12px;">
    <img src="static/images/logo.svg" alt="cobrando.lat" width="150px" height="150px">
    <h1 style="margin: 0; font-size: 48px;">Cobrando.lat</h1>
  </div>
</div>

<br>

Cobrando.lat es una plataforma web para compartir de forma segura tus datos de pago (cuentas bancarias, tarjetas, CLABE) sin exponer información sensible. Genera perfiles públicos únicos para que tus usuarios puedan pagar fácilmente.

## 🚀 Stack

- **Backend:** Django 5.2 + PostgreSQL 18
- **Frontend:** TailwindCSS 4
- **Deploy:** Docker + Gunicorn

## 🛠️ Desarrollo

### Requisitos

- Docker y Docker Compose instalados en tu máquina.

### Setup

1. **Clona el repo:**
   ```bash
   git clone https://github.com/ferdotdev/cobrando-lat.git
   cd cobrando-lat
   ```

2. **Crea tu `.env`:**

Edita las variables necesarias del archivo de ejemplo y crea tu .env

3. **Levanta el entorno de desarrollo:**

Usa el contenedor de desarrollo ya configurado en la carpeta .devcontainer

O bien, desde la terminal:
   ```bash
   cd docker/dev
   docker compose up
   ```

4. **Accede:** http://localhost:ENV_PORT

El servidor se recarga automáticamente con los cambios.

## 🚢 Deploy a producción

```bash
cd docker/prod
docker compose up -d
```

Asegúrate de configurar correctamente las variables de entorno en producción (`DEBUG=False`, `SECRET_KEY`, etc.).

## 📝 Licencia
Distribuido bajo la Licencia Pública General GNU GPL v3.0. Puedes usar, estudiar, modificar y redistribuir el código libremente.

Cualquier trabajo derivado debe publicarse bajo la misma licencia (copyleft). Consulta el texto completo en [LICENSE](LICENSE).