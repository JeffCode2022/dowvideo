# FlowGet - Descargador Universal de Videos y Audio

Una aplicación web ultra-premium, moderna y eficiente para descargar videos y audios de múltiples plataformas, construida con Flask y yt-dlp bajo una estética minimalista y limpia.

## 🚀 Características

- Interfaz de usuario intuitiva y responsive
- Soporte para múltiples plataformas de video
- Descarga automática en la mejor calidad disponible
- Validación de URLs
- Manejo de errores robusto
- Diseño moderno y amigable

## 🛠️ Tecnologías Utilizadas

- Python 3.x
- Flask 3.1.0
- yt-dlp 2024.12.6
- HTML5
- CSS3

## 📋 Prerrequisitos

- Python 3.x instalado en tu sistema
- pip (gestor de paquetes de Python)

## 🔧 Instalación

1. Clona el repositorio:
```bash
git clone https://github.com/tu-usuario/dowvideo.git
cd dowvideo
```

2. Crea un entorno virtual (recomendado):
```bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

3. Instala las dependencias:
```bash
pip install -r requirements.txt
```

## 🚀 Uso

1. Inicia la aplicación:
```bash
python app.py
```

2. Abre tu navegador y visita:
```
http://localhost:5000
```

3. Pega la URL del video que deseas descargar y haz clic en "Descargar Video"

## 📁 Estructura del Proyecto

```
dowvideo/
├── app.py              # Aplicación principal Flask
├── requirements.txt    # Dependencias del proyecto
├── templates/         # Plantillas HTML
│   └── index.html     # Página principal
├── downloads/         # Directorio para videos descargados
└── Procfile          # Configuración para despliegue en Heroku
```

## 🔒 Seguridad

- La aplicación valida las URLs antes de procesarlas
- Se implementan medidas de seguridad básicas de Flask
- Los archivos descargados se almacenan en un directorio específico

## 🌐 Plataformas Soportadas

La aplicación utiliza yt-dlp, que soporta múltiples plataformas incluyendo:
- YouTube
- Vimeo
- Facebook
- Instagram
- Twitter
- Y muchas más...

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Por favor, abre un issue primero para discutir los cambios que te gustaría hacer.

## 📝 Licencia

Este proyecto está bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE) para más detalles.

## ⚠️ Aviso Legal

Esta herramienta es para uso personal y educativo. Asegúrate de respetar los términos de servicio de las plataformas de video y las leyes de derechos de autor de tu país.

## 📞 Soporte

Si encuentras algún problema o tienes sugerencias, por favor abre un issue en el repositorio. 