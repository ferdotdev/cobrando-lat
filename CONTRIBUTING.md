# 📋 ¿Cómo Contribuir?

¡Gracias por tu interés en contribuir! Aquí te explicamos cómo hacerlo.

### 1. Crea tu fork

Crea el fork el repo en GitHub, tienes el enlace aqui: [cobrando.lat](https://github.com/ferdotdeb/cobrando-lat) 

### Crea una branch descriptiva:

Luego clona tu fork localmente y crea una branch nueva

```bash
git clone https://github.com/TU_USUARIO/cobrando-lat.git
cd cobrando-lat
git branch feature/mi-nueva-funcionalidad
```

Usamos convenciones semánticas para los nombres de las branches:

- `feature:` nueva funcionalidad
- `fix:` corrección de bugs
- `docs:` cambios en documentación
- `style:` formato, punto y coma, etc.
- `refactor:` refactorización de código
- `test:` añadir o modificar tests

Asi tu branch sera descriptiva y facil de identificar.

### 2. Configura tu Entorno

Sigue las instrucciones del [README.md](README.md) para levantar el entorno de desarrollo.

### 3. Haz tus Cambios

- Escribe código limpio y documentado
- Sigue las convenciones de Django y PEP 8
- Añade tests si es posible
- Asegúrate de que todo funciona antes de hacer commit

### 4. Commit y Push

```bash
git add .
git commit -m "(emoji) descripción clara de tu cambio"
git push origin feature/mi-nueva-funcionalidad
```

### 5. Crea un Pull Request

- Describe qué resuelve tu PR
- Enlaza issues relacionados si existen
- Espera el review

## 🎯 Convenciones

### Commits

Antes de hacer commit, asegúrate de que tu mensaje siga el siguiente formato:

Antes del mensaje recuerda usar gitmoji con el emoji correspondiente.

Puedes consultar [gitmoji.dev](https://gitmoji.dev/) para tener una buena referencia de que emojis usar en tus commits.

Asegúrate de que tus mensajes sean claros y concisos.

### Código

- **Python:** Sigue PEP 8
- **HTML/CSS:** Mantén consistencia con el código existente
- **Commits:** Mensajes claros y en español

## 🐛 Reportar Bugs

Abre un [issue](https://github.com/ferdotdeb/cobrando-lat/issues) con:

- Descripción clara del problema
- Pasos para reproducirlo
- Comportamiento esperado vs actual
- Screenshots si aplica

## 💡 Sugerencias

Las ideas son bienvenidas. Abre un issue con la etiqueta `enhancement` para discutirla antes de implementarla.

## ❓ Preguntas

Si tienes dudas, abre un issue con la etiqueta `question` o contacta al maintainer.