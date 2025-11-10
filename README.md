<div align="center">
  <div style="display: inline-flex; align-items: center; gap: 12px;">
    <img src="static/images/logo.svg" alt="cobrando.lat" width="150px" height="150px">
    <h1 style="margin: 0; font-size: 48px;">cobrando.lat</h1>
  </div>
</div>

<br>

cobrando.lat es una plataforma web para compartir de forma segura tus datos de pago (cuentas bancarias, tarjetas, CLABE) sin exponer información sensible. Genera perfiles públicos únicos para que tus usuarios puedan pagar fácilmente.

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
   git clone https://github.com/ferdotdeb/cobrando.lat.git
   cd cobrando.lat
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

4. **Accede:** http://localhost:puerto_configurado

El servidor se recarga automáticamente con los cambios.

## 🚢 Producción

```bash
cd docker/prod
docker compose up -d
```

Asegúrate de configurar correctamente las variables de entorno en producción (`DEBUG=False`, `SECRET_KEY`, etc.).

## 📝 Licencia

GPL-3.0 - Ver [LICENSE](LICENSE)
