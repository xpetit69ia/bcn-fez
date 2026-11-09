# Prototipo de fuentes de precios

Este prototipo añade dos vías separadas al monitor BCN–FEZ:

1. **Kiwi.com a través de API.SH**: API estructurada de terceros que consulta ofertas públicas de Kiwi.com. No es una API oficial de la aerolínea ni confirma el precio final en el sitio de venta.
2. **Playwright**: navegador Chromium automatizado para extraer texto de una página únicamente cuando el acceso automatizado esté permitido y se haya configurado una URL y selector de resultados válidos.

## Configuración de Kiwi/API.SH

1. Crear una cuenta en https://api.sh/ y obtener una clave.
2. En GitHub, abrir Settings → Secrets and variables → Actions.
3. Crear el secreto `APISH_API_KEY`.
4. Ejecutar Actions → “Prototype - Kiwi API and authorized browser probe”.
5. Introducir origen, destino y fecha. El prototipo busca una ventana de 15 días en una sola llamada.

La página de API.SH indica 1.000 créditos gratuitos mensuales por cuenta y un coste de 1 crédito por llamada al endpoint Kiwi Flights. Revisar siempre el panel de cuenta y las condiciones vigentes antes de usarlo de forma recurrente: https://api.sh/docs/kiwi-flights

## Configuración de Playwright

El navegador está preparado, pero no se activa hasta que se configuren estos secretos:

- `BROWSER_SEARCH_URL_TEMPLATE`: URL de resultados autorizada. Puede contener `{origin}`, `{destination}` y `{date}`.
- `BROWSER_PRICE_SELECTOR`: selector CSS que identifica los bloques de precio en esa página.

Ejemplo ilustrativo de plantilla (no es una URL de aerolínea validada):
`https://example.com/flights/{origin}/{destination}?date={date}`

No configurar un dominio hasta revisar sus condiciones y obtener autorización cuando corresponda. El script no resuelve CAPTCHAs, no evade bloqueos, no inicia sesión y no intenta acceder a endpoints internos. Si detecta una pantalla de verificación o bloqueo, se detiene.

## Resultados

- `data/kiwi-results.json`
- `data/browser-probe-results.json` (solo si Playwright está configurado)

Los dos resultados se marcan como `unverified`. Las ofertas de un agregador deben revalidarse con el vendedor antes de presentarlas como disponibles o confirmadas. Este prototipo no modifica los datos históricos ni la consulta diaria de Ignav.
