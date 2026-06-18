\# Skills de Orquestación y Agentes Autónomos



Este archivo define las reglas avanzadas para el diseño de agentes conversacionales, flujos de trabajo autónomos y conexiones de API robustas.



\## 1. Arquitectura de Agentes Conversacionales

\- \*\*Flujos de Estado:\*\* Al diseñar lógica para agentes autónomos que manejen conversaciones o árboles de decisión complejos, estructura el código utilizando máquinas de estado claras o grafos de persistencia de estado para evitar la pérdida de contexto.

\- \*\*Estandarización de Payloads:\*\* Toda comunicación entre APIs externas y endpoints locales debe manejar payloads JSON estrictamente estructurados.

\- \*\*Validación Estricta:\*\* Utiliza `Pydantic` de forma obligatoria para validar los esquemas de datos entrantes y salientes en cada webhook o integración de API, asegurando un tipado seguro.



\## 2. Integración de Servicios de Voz y Telefonía

\- \*\*Manejo de Audio Digital:\*\* Al interactuar con microservicios de clonación de voz o síntesis de audio (como ElevenLabs), asegúrate de configurar correctamente los headers de streaming para evitar latencias en la respuesta.

\- \*\*Parámetros de Red y SIP:\*\* Si el script incluye configuraciones para troncales SIP o pasarelas de voz (como configuraciones estilo Parloa o n8n), documenta y valida los timeouts de conexión para prevenir caídas en las llamadas en tiempo real.



\## 3. Resiliencia de Webhooks

\- Todo endpoint diseñado para recibir alertas de orquestadores debe incluir un sistema de reintentos (\*retries\*) con retraso exponencial ante fallos de red 5xx.

