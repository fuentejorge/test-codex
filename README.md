# Buscador de JPGs

Aplicacion en Python que busca archivos `.jpg` y `.jpeg` en el equipo y genera
un inventario en un archivo de texto con directorio, nombre y tamano en bytes.

## Cambios implementados

- Escaneo de todos los discos logicos por defecto.
- Salida fija en `C:\temp\jpg_inventory.txt` si no se especifica otra ruta.
- Creacion automatica del directorio de salida si no existe.

## Requisitos

- Python 3.8+
- Windows

## Uso

```bash
python find_jpgs.py
```

Opciones:

```bash
python find_jpgs.py --output C:\temp\salida.txt
python find_jpgs.py --roots C:\ D:\Fotos
python find_jpgs.py --jpg-only
```

## Formato de salida

El archivo genera un encabezado y luego una fila por imagen:

```text
directory	filename	size_bytes
C:\ruta	imagen.jpg	12345
```
