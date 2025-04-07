# 📷 ServitelWeb

**Sitio web desarrollado con Django para una empresa de cámaras de seguridad.**  
Presenta productos, permite solicitudes de clientes y gestiona un panel de administración completo, con integración de filtros, correo automático y lógica de seguridad.

---

## 🧰 Tecnologías utilizadas

- **Backend:** Django (Python)
- **Frontend:** HTML5, CSS3, JavaScript
- **Base de datos:** SQLite (por defecto de Django)
- **Estilos personalizados:** `navstyle.css`, `index.css`, etc.
- **API de correos:** [MailerSend](https://www.mailersend.com/)

---

## 🏠 Funcionalidades del sitio

### Página de inicio (`index.html`)
- Banner principal con producto destacado.
- Navbar con logo y enlaces a:
  - Catálogo
  - Cámaras
  - Accesorios
- Carrusel dinámico de productos recientes (desde la base de datos).
- Al hacer clic en una tarjeta, se accede al detalle del producto.

### Accesos directos
- Botones visibles en la portada para ir directo a:
  - Catálogo completo
  - Sección de cámaras
  - Productos de accesorios

### Catálogo (`catalogo.html`)
- Lista de productos mostrados como tarjetas.
- Datos cargados dinámicamente desde la base de datos.
- Filtros por:
  - Cantidad de cámaras
  - Cantidad de canales del DVR

### Accesorios
- Página que muestra automáticamente solo productos clasificados como accesorios.
- Filtrado interno mediante funciones en `views.py` y `models.py`.

---

## 🛒 Lista de deseos (tipo carrito de compras)

- Cada producto se puede agregar a una lista de deseos.
- El usuario puede:
  - Modificar la cantidad
  - Ver la lista desde un panel lateral dinámico (no cubre toda la pantalla)
- Toda la lógica funciona con JavaScript.
- Al confirmar, la lista se envía como una solicitud a la base de datos.

---

## 🧑‍💼 Panel de administración

- Acceso protegido (solo usuarios autenticados y con permisos).
- Funcionalidades:
  - Agregar, editar y eliminar productos del catálogo.
  - Ver solicitudes de clientes.
  - Cambiar estado de cada solicitud:
    - Confirmada
    - En proceso
    - Entregada
    - Cancelada
- Cada cambio de estado genera un correo automático al cliente.

---

## 📬 Envío de correos

- Se utiliza la API de **MailerSend** para:
  - Confirmación de solicitudes
  - Notificación de cambio de estado
  - Recuperación de contraseña con token

---

## 🔐 Seguridad

- No permite acceso con credenciales incorrectas.
- Bloqueo del acceso a la URL del panel si no hay sesión de administrador activa.
- Función de recuperación de contraseña:
  - El usuario solicita un correo
  - Recibe un token
  - Accede a un formulario para crear nueva contraseña
  - Los datos se actualizan en la base de datos

### 📁 Estructura principal del proyecto

> **Nota:** En esta sección se omiten archivos como `models.py` y `admin.py` para centrarse solo en la estructura general del proyecto.

```
ServitelWeb/
├── core/                      # Lógica principal del sitio (catálogo, inicio, filtros)
│   ├── templates/core/        # Plantillas HTML específicas de esta app
│   ├── static/core/           # Archivos estáticos propios de esta app (js, css, images)
│   └── urls.py                # Rutas específicas de la app
│
├── crud/                      # CRUD de productos desde el panel de administrador
│   ├── templates/crud/        # Plantillas HTML para gestionar productos
│   ├── static/crud/           # Archivos estáticos propios de esta app (js, css, images)
│   └── urls.py                # Rutas específicas de la app
│
├── login/                     # Autenticación y gestión de usuarios
│   ├── templates/login/       # Plantillas HTML para login y gestión de usuarios
│   ├── static/login/          # Archivos estáticos propios de esta
```

---
## ✨ Notas finales

Este proyecto fue creado como parte de mi portafolio para mostrar el uso profesional de Django, el manejo de templates, integración de JavaScript, lógica de seguridad y comunicación con el cliente. Está pensado para empresas pequeñas que buscan una solución funcional, segura y moderna para mostrar y gestionar sus productos.

---

## 👩‍💻 Desarrollado por

**Fernanda Valenzuela**

