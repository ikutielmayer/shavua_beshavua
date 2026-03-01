# Shavua BeShavua 🕍

Una plataforma interactiva de estudio de Torá, Halajá y Tzedaká semanal con sistema de premios y gamificación.

## Características 🚀

- **Estudio de Parashá**: Preguntas dinámicas semanales basadas en la Parashá actual.
- **Estudio de Halajá**: Categorías de estudio (Shabat, Kashrut, Tefilá) con generación infinita de preguntas.
- **Sistema de Puntos**: Acumula puntos por respuestas correctas y entra en sorteos mensuales.
- **Sorteos**: Sistema automatizado de sorteo de premios basado en la participación y donaciones.
- **Publicidad**: Gestión de anuncios multi-línea para patrocinadores locales.
- **Multilingüe**: Soporte completo para Español, Inglés y Hebreo (con soporte RTL).
- **Responsive**: Optimizado para computadoras, tablets y dispositivos móviles.

## Instalación 🛠️

1. **Clonar el repositorio:**
   ```bash
   git clone https://github.com/tu-usuario/shavua-beshavua.git
   cd shavua-beshavua
   ```

2. **Crear y activar entorno virtual:**
   ```bash
   python -m venv venv
   source venv/Scripts/activate  # En Windows
   # o
   source venv/bin/activate       # En Linux/Mac
   ```

3. **Instalar dependencias:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configurar variables de entorno:**
   Copia `.env.example` a `.env` y completa tus credenciales de base de datos y correo:
   ```bash
   cp .env.example .env
   ```

5. **Configurar la base de datos:**
   Asegúrate de tener MySQL corriendo y ejecuta los scripts en la carpeta `scripts/` para inicializar las tablas y cargar el banco de preguntas.

## Ejecución 🏃‍♂️

Para iniciar el servidor de desarrollo:
```bash
python run.py
```
El sitio estará disponible en `http://localhost:5001`.

## Estructura del Proyecto 📁

- `app/`: Contiene toda la lógica de la aplicación (modelos, rutas, plantillas).
- `scripts/`: Herramientas para mantenimiento, migración e inicialización de datos.
- `static/`: Archivos CSS, imágenes y recursos frontal.
- `templates/`: Plantillas HTML (Jinja2).

## Licencia 📄
Este proyecto es de uso privado. Todos los derechos reservados.
