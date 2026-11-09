# Acceso autorizado a tarifas de aerolíneas

Estado revisado: 2026-11-09

Objetivo: consultar tarifas de solo ida desde GitHub Actions para mostrarlas en el panel BCN–FEZ, sin automatizar la navegación por páginas web de aerolíneas.

## Resultado de la comprobación

| Aerolínea | Vía identificada | ¿Acceso gratuito confirmado? | Próximo paso |
|---|---|---:|---|
| Ryanair | Licencia de datos/API o socio aprobado | No | Solicitar autorización por escrito para consulta y comparación de tarifas. No hacer scraping. |
| Vueling | Distribución NDC mediante proveedores de servicios; portal Vueling Partners | No | Consultar a Vueling si admite acceso NDC directo o de pruebas para un proyecto no comercial y qué proveedor/contrato requiere. |
| Air Arabia Maroc | Portal oficial para agentes/partners de Air Arabia | No | Solicitar condiciones de alta como partner y confirmar si existe acceso API/NDC de solo consulta para Air Arabia Maroc. |

### Ryanair

Las condiciones oficiales de Ryanair indican que las páginas de comparación pueden solicitar una licencia escrita para acceder a precios, vuelos y horarios. También restringen la extracción automatizada sin autorización. Por tanto, no se implementará scraping ni el uso de endpoints internos no documentados.

Referencia: https://www.ryanair.com/es/es/lp/legal/condiciones-de-uso

### Vueling

Vueling publica documentación de funcionalidades NDC disponibles a través de proveedores de servicios, incluyendo Air Shopping y Flight Calendar (precios y rutas). La documentación no confirma que un proyecto particular pueda obtener credenciales gratuitas ni acceso directo sin intermediario. El portal Vueling Partners está orientado a clientes/agencias y sus condiciones prohíben automatizar su plataforma sin autorización expresa.

Referencias:
- https://static.vueling.com/blogpartners/media/1103/vy-ndc-_-partners-services-and-functionalities.pdf
- https://partners.vueling.com/web/es-ES/Register/

### Air Arabia Maroc

Air Arabia dispone de un portal oficial para agentes de viaje y partners, que incluye Air Arabia Maroc. La página pública no confirma una API gratuita ni credenciales de consulta para desarrolladores independientes.

Referencia: https://www.airarabia.com/en/about-us/travel-agents-portal

## Diseño previsto en BCN–FEZ

1. Mantener Ignav como fuente actual y de respaldo.
2. Añadir un adaptador independiente por proveedor autorizado, ejecutado desde GitHub Actions.
3. Normalizar cada observación con: origen, destino, fecha de salida, aerolínea/proveedor, precio, moneda, fecha de consulta, estado y fuente.
4. No guardar credenciales en el repositorio: usar GitHub Actions Secrets.
5. Diferenciar claramente tarifa observada, tarifa revalidada y error/sin acceso.
6. No mostrar una tarifa como confirmada hasta que el proveedor permita revalidarla.

## Bloqueo actual

No se han encontrado credenciales públicas gratuitas y utilizables de forma inmediata para estas tres aerolíneas. Antes de programar conectores reales hacen falta credenciales, documentación de API y condiciones de uso confirmadas. No se añadirán conectores ficticios ni automatización de páginas web que pueda incumplir las condiciones de las compañías.
