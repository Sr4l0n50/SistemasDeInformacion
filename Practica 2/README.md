# Práctica 2: Representación de los datos

En esta segunda práctica de la asignatura simularemos el proceso de creaci  ́on de un dashboard o
Cuadro de Mando Integral (CMI). Este dashboard es una representaci  ́on visual de los datos obtenidos
tras el tratamiento realizado en la primera pr  ́actica, y lo desarrollaremos utilizando el lenguaje de
programaci  ́on Python. Adem  ́as, se plantear  ́an un conjunto de preguntas relacionadas con el dise  ̃no
e implementaci  ́on de nuestro sistema OLAP. La pr  ́actica se realizar  ́a en los mismos grupos creados
para la primera pr ́actica. La pr ́actica s ́olo debe ser entregada por un integrante.

## 2 Entorno de la pr ́actica
En esta práctica seguiremos trabajando en el mismo entorno que la práctica anterior. Nuestros
clientes nos han felicitado tras desarrollar el sistema MIS.
El problema es que los informes que hemos generado son estáticos (si nos env ́ıan datos a tiempo
real, no podemos representarlos), y no permiten personalizar los diagramas. Por ello, ahora quieren
que dise  ̃nemos el almac ́en de datos. Para despu ́es dise  ̃nar un CMI que facilite la toma de decisi  ́on a
la direcci ́on de la empresa.

## 3 Ejercicio 1 [0 puntos] - Revisar el ejercicio 6
Este ejercicio ha sido renombrado como ejercicio 6 para no tener que renombrarlos en vuestra
memoria.

## 4 Ejercicio 2 [1 punto]
Para simular el CMI usaremos la librería de Flask en Python. En este ejercicio, se desarrollarán los
procedimientos necesarios para que el usuario muestre por pantalla los siguientes valores.
* El top X de usuarios críticos. (0.5)
* El top X de páginas web vulnerables. (0.5)

## 5 Ejercicio 3 [1.5 puntos]
Ahora deberemos crear los procedimientos necesarios para que el CMI pueda visualizar el top X
de usuarios cr ́ıticos, pero también podrá seleccionar si desea que se muestre la información de los
usuarios que tienen han pulsado m ́as del 50% de veces al correo de spam o menos del 50%.

## 6 Ejercicio 4 [1.5 puntos]
Mostrar las  ́ultimas 10 vulnerabilidades basado a tiempo real. En la siguiente web https://www.
cve-search.org/api/ nos muestra esta información y para estar actualizados se pide que nuestro
CMI tenga esta información.

## 7 Ejercicio 5 [3 puntos]
Este ejercicio será un ejercicio libre. Cada equipo decidirá qué añadir a su CMI para que genere
información de valor.
Algunos ejemplos:
* Sistema de login para usuarios.
* Generaci ́on de informes en PDF.
* An ́alisis de otras métricas (conexiones por día de usuario, etc.)
* Mostrar datos de alg ́un servicio web mediante otra API.
* Modelo basado en inteligencia artificial que detecte si un usuario es crítico o no.
Cabe resaltar que este ejercicio es completamente opcional. En caso de que un equipo no realice este
ejercicio, podría obtener una nota máxima de 7 puntos en la evaluación de esta práctica.

## 8 Ejercicio 6 [3 puntos]
Basado en los modelos de aprendizaje supervisados vistos en el tema 6 realizaremos un algoritmo
que dado un usuario nuevo detecte si va a ser un usuario cr ́ıtico o no.
Para ello, con el conjunto de datos inicial sabiendo si un usuario es cr ́ıtico o no realizaremos diferentes
m ́etodos de clasificaci ́on.
Utilizaremos https://scikit-learn.org/ scikit learn para desarrollar este  ́ultimo ejercicio.
* Realizar un método de Regresión Lineal (1 punto)
* Realizar un método de Decision Tree (1 punto)
* Realizar un método de Random forest (1 punto)
Se os adjuntar  ́a un nuevo archivo con usuarios, para determinar si esos usuarios son cr ́ıticos o no,
teniendo que devolver cuantos usuarios son críticos y cuantos no lo son.
El prop  ́osito de cada ejercicio demás de obtener un algoritmo de inteligencia artificial, será documen-
tar gráficamente como obtiene la clasificaci ́on cada uno de los algoritmos.

## 9 GitHub
Será de uso obligatorio la creación de un repositorio de GitHub para la realización de las prácticas
con los miembros del grupo.

## 10 Material a entregar
La entrega de la pr ́actica consistir ́a en un archivo comprimido con los siguientes ficheros:
* Carpeta src del proyecto de PyCharm.
* Archivo SQLite con la base de datos creada.
* Memoria en formato PDF en la que se responda al ejercicio 1, y se justifique las decisiones
tomadas en todos los ejercicios. En caso de resolver el ejercicio 5, las implementaciones deber  ́an
estar incluidas.
* La memoria debe incluir el nombre y apellidos de los integrantes del grupo y el enlace al
repositorio de GitHub.

