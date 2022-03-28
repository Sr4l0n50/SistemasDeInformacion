# Practica 1: Recopilación, estructuración y análisis de resultados
El objetivo de esta primera practica es el de profundizar en algunos de los conceptos vistos en las sesiones de teoría. La situacion que se plantea es la siguiente: acabas de entrar en una gran companñia que proporciona servicio de auditorías. Tu labor dentro de la companñia sera analizar algunos procesos del modelo de negocio y desarrollar un pequeno sistema de información. En la empresa tienen definidos una gran variedad de procesos, pero para esta practica nos interesa el proceso mediante el cual se decide si trabajar con una empresa o no. Este proceso de negocio por el cual se evalua si trabajar con una empresa o no comienza cuando la empresa interesada en los servicios de auditoría, manda diferentes archivos a través del departamento de contrataciones, esto archivos son:
* 1) informe de usuarios con el log de sesiones, hash de sus contrasenas, permisos, datos personales, etc
* 2) el listado de paginas webs que tiene la empresa. En ese momento, ese email se reenvía al director del servicio de auditorías que se encargara de verificar si los archivos que se han enviado son correctos, y decidir si continua el analisis de la empresa adelante o no. Si el director no da su visto bueno, el departamento de contrataciones contestara al email del cliente con la respuesta negativa. En caso contrario, sera el propio director el que mandará los documentos a los diferentes departamentos, para que realicen un analisis de la empresa:
* **Departamento de formacion de personal.** La compañía tiene un departamento encargado de analizar los perfiles de los usuarios de la empresa. En este punto se evaluar varios aspectos: 1) complejidad de las contrasenas (mediante el hash), y 2) emails de spam que ha recibido e interactuado. Este departamento realizara un reporte de usuarios críticos y lo adjuntaran al departamento de contrataciones.
* El segundo departamento que recibe los documentos sera el servicio **responsable de legal**, tiene como tarea verificar el cumplimiento de todas las políticas legales en los diferentes servicios webs. En concreto, analizara si las webs disponen de cookies, aviso legal y protección de datos. Completara el archivo enviado con los datos por cada página y este informe ser recibido por el departamento de contrataciones.
* Por ultimo, el **departamento de inteligencia artificial** evaluara las conexiones a los servicios de la empresa por parte de los usuarios y reportara el número estimado sin profundizar de características críticas de la empresa. Una vez tenga este numero de características críticas, adjuntará al departamento de contrataciones un informe.
* El **departamento de contrataciones**, ademas de establecer la comunicación inicial con el cliente, se encargara de determinar el presupuesto y tiempo de trabajo necesario, basado en el número de características/vulnerabilidades encontradas en el sistema del cliente.

Cuando el departamento de contrataciones hayan finalizado su informe final, le mandaran su conclusión al director. Si el director recibe un “Sí” por parte del departamento de contrataciones, analizara los proyectos donde se está trabajando para poder determinar si se tiene personal para comenzar a trabajar con la empresa, en caso de no tener personal remitira un correo al departamento de contrataciones para que respondan con un “Sí” y la fecha en la que se puede comenzar a realizar el
proyecto, en caso de tener personal respondera con un “Sí” mostrando que se puede comenzar cuanto antes y en caso de ver en el informe poca cantidad de vulnerabilidades/caracter´ısticas reportara un “No” debido a que sera un trabajo breve con el cual no quiere dedicar tiempo. Finalmente, el departamento de contratacion le comunicará al cliente toda la información: si es viable su proyecto, el inicio del proyecto y el presupuesto estimado. La primera tarea dentro de esta compañía sera la de modelar, usando BPMN y UML, este proceso de negocio que se acaba de describir. La segunda tarea que te han encomendado es la de desarrollar, una primera version de un sistema de información gerencial o MIS (Management Information System). Para ello, se te proporcionan los archivos JSON extraído de sus base de datos. Tu labor sera la de desarrollar, usando el lenguaje de programación Python y una base de datos SQLite, este pequeno MIS que genere la información que se detalla en los diferentes ejercicios de este enunciado. Ademas, se pondrá en práctica el uso de librerías pensadas para realizar un analisis de datos que permita generar información interesante para un potencial usuario final, cliente o, simplemente, alguien interesado en recibir la informacion que se obtiene tras el filtrado y analisis de los datos proporcionados. Concretamente, utilizaremos la librería Pandas para ayudarnos a realizar esta tarea. Es importante que el alumnado realice esta primera practica con éxito y de forma adecuada, ya que la segunda practica se basará en gran medida en los resultados, o avances alcanzados en esta practica. La práctica se realizará en grupos de 3 personas. La practica solo debe ser entregada por un integrante

## 2 conjunto de datos
Para esta practica, utilizaremos el archivo de material adicional, el cual contiene diferentes archivos JSON.
* **legal.json** contiene el analisis realizado por el departamento de legal de cada una de las webs.
* **users.json** contiene la informacion de cada uno de los usuarios de la empresa.

## 3 Ejercicio 1 [3 puntos]
En este primer ejercicio, el grupo debera desarrollar el modelado del proceso de negocio descrito anteriormente usado las dos notaciones vistas en teoría: Business Process Modeling Notation (1.5 punto) y Unified Modeling Language (1.5 punto)

## 4 Ejercicio 2 [2 puntos]
El objetivo de este ejercicio sera el de desarrollar un sencillo sistema ETL. No es necesario desarrollar las fases de extraccion ya que disponemos del archivo JSON. Debemos diseñar las tablas en la base de datos y desarrollar los codigos necesarios para leer los datos del fichero JSON y almacenarlos en la base de datos. Después, sera necesario leer los datos desde la BBDD (usando diferentes consultas) y se almacenaran los resultados en un DataFrame para poder manipularlos. En este ejercicio, para el correcto desarrollo del sistema MIS, sera necesario calcular los siguientes valores: 
* Numero de muestras (valores distintos de missing).
* Media y desviacion estándar del total de fechas que se ha iniciado sesión.
* Media y desviacion estándar del total de IPs que se han detectado.
* Media y desviacion estándar del número de emails recibidos.
* Valor mínimo y valor maximo del total de fechas que se ha iniciado sesión.
* Valor mínimo y valor maximo del número de emails recibidos.

## 5 Ejercicio 3 [2.5 puntos]
Hay datos que nos interesa analizar basandonos en agrupaciones, para darle un sentido a nuestro analisis en base a esa agrupación. De una manera más específica, vamos a trabajar con las siguientes agrupaciones:
* Por tipo de permisos de usuario (0 equivalente a usuario y 1 equivalente a administrador)
* Número de emails recibidos: estableceremos dos rangos diferentes, el primero aquellos contenidos que tengan menos de 200 correos, y aquellos que tengan igual o mas de 200 correos.
En este caso deberemos calcular la siguiente informacion para la variable dentro del email de phishing:
* Numero de observaciones
* Numero de valores ausentes (missing)
* Mediana
* Media
* Varianza
* Valores maximo y mínimo

## 6 Ejercicio 4 [2.5 puntos]
Por ultimo, se programarán las diferentes funciones del MIS. En concreto, se deben generar gráficos sencillos para obtener los siguientes datos:
* Mostrar los 10 usuarios mas críticos (un usuario cr´ıtico es aquel usuario que tiene la contraseña débil y ademas tiene mayor probabilidad de pulsar en un correo de spam), representadas en un gráfico de barras.
* Mostrar las 5 paginas web con que tienen más políticas (cookies, protección de datos o aviso legal) desactualizadas, representadas en un grafico de barras según las políticas.
* Mostrar la media de conexiones de usuarios con contrasena vulnerable, frente a los que no son vulnerables.
* Mostrar segun el año de creación las webs que cumplen todas las políticas de privacidad, frente a las que no cumplen la política de privacidad.
* Mostrar el numero de contraseñas comprometidas y contraseñas no comprometidas. 

## 7 GitHub
Sera de uso obligatorio la creación de un repositorio público de GitHub para la realización de las prácticas con los miembros del grupo. Es recomendable el uso correcto de GitHub, se valorará negativamente la incorporacion de todos los datos en un solo commit. 
