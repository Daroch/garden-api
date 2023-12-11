# garden-api

Garden Api development in Python to Devcamp Capstone Project to work with Garden App

El objetivo de la aplicación es poder realizar un seguimiento a nuestras plantas, bien sean plantas ornamentales en casa o distintos cultivos en una huerta.
El sistema nos avisará de forma automática, cuando se produce algún hito importante en alguna planta (por ejemplo necesidades de riego, abono, fechas de siembra/transplante/recolección

Cada plantra tendrá una ficha con información básica que podemos editar, así como un diario donde añadiremos actualizaciones de estado o nuevas fotos de nuestra planta.

## Main Feature

El sistema enviará avisos (Desktop notifications meidante websocket) al usuario relativos a distintos eventos cada “x” dias, en función de la frecuencia que hallamos configurado para una planta y ese evento determinado:
Ejemplos:
Aviso de riego, de abonado, de antiplagas, de siembra, de recolección, de epoca de trasnplante.

- funcion que calcula los dias desde el ultimo riego/abonado/evento y envia una notificación al navegador,

## Extras

- Buscador en la app, que muestra resultados, filtrando por nombre planta, clima, (otros campos), que sea publica, y permite clonar la planta a nuestro garden, con sus datos recomendados (en principio sin clonar las fotos). → Añade fotos de tu nueva planta!
- Posibilidad de ver todas las plantas de un usuario?(si son publicas)

- Mapa ubicaciones: si la planta tiene introducidas coordenadas de ubicación, podria usarse para añadir árboles (o setas) y posicionarlos en un mapa.

---

### Tecnologías a utilizar:

**App principal:**

- Desarrollada en React/Javascript
- Maquetación CSS
- Comunicación mediante archivos JSON.
- Llamadas via Axios a una API

**API**

- Generada con Python + FastAPI + SQLAlchemy

**Backend**

- Python→¿Django?
- Base de datos MySQL

Repositorios Git independientes para Frontend y Backend

Best practiques

- Control Structures (login, user capabilities)
- RESTFUL APIs
- Test Driven
- Software (Vscode, MySQLWorkbench, Modelio)
- Code Quality (Vscode plugins ESLINT, prettier)
- UML Diagrams with Modelio

---

### UML DIAGRAMS

**Use Case**
![Use Case](<uml-images/plants manager Use Case diagram.png>)

**Activity Diagram**
![Alt text](<uml-images/Garden App Activity diagram.png>)

**Class Diagram**
![Alt text](<uml-images/Garden Manager Class diagram.png>)
