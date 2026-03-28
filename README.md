# Fase 1: implementación

## Introducción

Esta investigación busca el desarrollo de un modelo de aprendizaje automático que sea capaz de identificar si un mensaje SMS en Guatemala es malicioso o no haciendo uso de 3 vectores de ataque: 

- El contenido del mensaje
- El emisor del mensaje
- Metadata asociada al mensaje como presencia de URLs, longitud del mensaje, presencia de palabras de ugencia, etc

Sin embargo, en Guatemala no se ha realizado mucha investigación al respecto y no hay datos oficiales o datasets que tengan registro de los mensajes de texto que tengan una intención maliciosa. Tampoco existen bases de datos que contengan mensajes con información legítima como comprobantes de pago, solicitudes código de verificación, etc. Por esa razón, en este informe se enumeran los procedimientos realizados para generar un dataset que contenga esta información

## Parte 1: Obtención de datos

Este tipo de estafas son muy frecuentes en Guatemala, por lo que gran parte de los ciudadanos guatemaltecos han recibido alguna vez un mensaje de texto con intención maliciosa. Por lo tanto, se decidió hacer una encuesta a una parte de la población guatemalteca en la que se recopila información sobre los mensajes sospechosos o maliciosos que hayan recibido alguna vez, en la encuesta también se pide información de mensajes legítimos como promociones de empresas telefónicas y restaurantes, comprobantes de transacciones bancarias o solicitudes de autenticación. Cabe aclarar que todos los datos recopliados en la encuesta fueron anónimos y que los participantes aceptaron compartir la información de sus mensajes recibidos de forma voluntaria. 

La encuesta fue respondida por un total de 40 participantes, de los cuales 39 aceptaron participar voluntariamente.

La encuesta contenía 7 preguntas, a continuación se describe el propósito de cada una de ellas y los resultados obtenidos:

1. Consentimiento de participación

Pregunta:
¿Aceptas participar voluntariamente en esta encuesta?

Posibles respuestas:

Sí
No

Resultados:

![image1](imgs/survey_1.png)

<div align="center">
  <img src="imgs/survey_1.png" width="500"/>
  <p><em>Figura 1: Resultados de la encuesta</em></p>
</div>

Propósito:
Garantizar que la participación en la encuesta sea completamente voluntaria y cumplir con principios éticos de recolección de datos.

2. Experiencia con SMS sospechosos

Pregunta:
¿Ha recibido alguna vez un SMS que le pareció sospechoso?

Resultados:

Sí: 38
No: 2

Propósito:
Determinar la prevalencia de este tipo de mensajes en la población y validar la relevancia del problema en el contexto guatemalteco.

3. Identidad del remitente

Pregunta:
¿De quién decía ser el mensaje?

Resultados principales:

Empresa de paquetería o envíos: 10
Operadora telefónica: 6
Institución del gobierno: 5
Empresa o empleador: 5
Banco o entidad financiera: 4
No identificado / desconocido: 7

Propósito:
Identificar los tipos de entidades que los atacantes suelen suplantar, lo cual permite definir características relevantes para el modelo de clasificación.

4. Tipo de estafa

Pregunta:
¿A qué categoría pertenece la estafa que intentaron hacerle?

Resultados principales:

Paquetes y envíos: 13
Premios y recompensas: 8
Servicios y trabajo: 6
Otras categorías: menor frecuencia

Propósito:
Clasificar los distintos tipos de ataques y entender los patrones más comunes utilizados en mensajes maliciosos.

5. Ejemplo de SMS sospechoso

Pregunta:
Escriba el texto del primer SMS sospechoso que recibió.

Respuestas obtenidas:
29 respuestas válidas.

Ejemplos:

"No hemos logrado contactarlo, visite el siguiente link para coordinar la entrega de su paquete."
"Remitente desconocido: <#> 64763 es tu código de confirmación de Facebook..."

Propósito:
Recopilar datos reales para construir el dataset de mensajes maliciosos que será utilizado en el entrenamiento del modelo.

6. Ejemplo de SMS legítimo

Pregunta:
Escriba el texto de un SMS legítimo que haya recibido recientemente.

Respuestas obtenidas:
35 respuestas válidas.

Ejemplos:

"Consumo PROMERICA... Monto 2,000 quetzales..."
"BANRURAL: Amigo, en cajero automático se debitó de tu cuenta..."

Propósito:
Obtener ejemplos de mensajes legítimos para entrenar el modelo y evitar sesgos en la clasificación.

7. Tipo de mensaje legítimo

Pregunta:
¿De qué tipo es el mensaje legítimo?

Resultados principales:

Promociones de operadoras: 14
Notificaciones bancarias: 8
Confirmaciones de compra o entrega: 5
Códigos de verificación (2FA): 3

Propósito:
Categorizar los mensajes legítimos y comprender sus características para diferenciarlos de los mensajes maliciosos.


### Primera pregunta

-  ¿Aceptas participar voluntariamente en esta encuesta? 

Posibles respuestas: 

- Si
- No

Propósito: 



En la sección de anexos se puede ver más a detalle los resultados obtenidos en esta encuesta. 


## Parte 2: Limpieza y generación sintética

## Parte 3 

