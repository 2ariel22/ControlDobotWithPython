<h1 align="center">Control Dobot MG400 with Python</h1>

<h2 align="center"><img src="https://github.com/user-attachments/assets/541d178a-53a5-4200-850f-9d9a18b3310f" width="400"></h2>

<h3 align="center">Introducción</h3>
<p>En el presente proyecto, se ha desarrollado un programa en Python que permite el control del brazo robótico Dobot mediante la comunicación TCP-IP. Este sistema ofrece una interfaz interactiva a través de un menú en consola, brindando al usuario diversas opciones para gestionar el robot de manera eficiente. Entre las funcionalidades implementadas, se incluyen la habilitación y deshabilitación del robot, la visualización de coordenadas y el estado de entradas y salidas digitales, así como la capacidad de activar o desactivar salidas. Este enfoque facilita la interacción y el monitoreo del robot, permitiendo a los usuarios experimentar y aprender sobre su funcionamiento de forma práctica.</p>


## :hammer: Funcionalidades del proyecto<br>
<h3>Para cualquiera de las funcionalidades mencionadas a continuacion se debe acceder atravez del menu que esta por consola</h3>
<div align="center"><img src="https://github.com/user-attachments/assets/bd39c232-d8ea-44eb-bbc5-48c262ffb266" width="242"></div><br><br>

- Funcionalidad 1: Activar o desactivar robot<br>
  <div align="center">
    <h4>Desactivado</h4>
    <img width="400" src="https://github.com/user-attachments/assets/806e8954-1a2b-4af2-b23d-f5bf7805acb8">
    <p>El modo desactivado se caracteriza por una luz azul intermitente y nos permite mover el robot libremente al presionar el boton Unlock ubicado en el brazo del Dobot</p>
    <h4>Activado</H4>
    <p>Este modo en necesario para mover el robot mediante instruciones desde python y se caracteriza por una luz verde. Importante recordar que en este modo no sera posible mover el robot atravez del boton Unlock</p>
    <img width="400" src="https://github.com/user-attachments/assets/46326355-ecb6-4d3a-b083-0cbbd6de478c">

  </div><br><br>

- Funcionalidad 2: Guardar posicion actual<br>
  <div>
    <p>Para guardar la posicion actual hay que seguir unos pasos, los cuales son:<br>
  <div>
    1.Desactivar el robot.<br>
    2.Ubicar el robot en la posicion de interes. <br>
    3.Presionar la opcion 4 en el menu.<br>
    4.Presionar la opcion 5.<br>
  </div>
  Una vez realizados estos pasos ya tendremos guardada la posion actual<br>
  </p>

  </div>
  
- Funcionalidad 3: Ir a posicion guardada<br>
  <div>
    <p>Para ejecutar esta funcionalidad basta con presionar la opcion numero 9</p><br>

  </div>

## Video de ejemplo
<div align="center">
  <a href="https://youtu.be/IQ-Qc7uZi4Y">
    <img src="https://img.youtube.com/vi/IQ-Qc7uZi4Y/0.jpg" alt="YouTube" width="450">
  </a>
</div>

## 📁 Acceso al proyecto
*Debes ejecutar el archivo "PresentacionMañana.py" ubicado en la carpeta src. Recuerda reemplazar la ip por la de tu Dobot.*

## 🛠️ ejecuta el proyecto

*Nota: Debes estar en la misma red wifi.*

## :hammer: Tecnologías utilizadas
- Python 3.12.3

## :book: Librerías utilizadas
- threading
- dobot_api

## Autores
<div align="center">
  <img src="https://avatars.githubusercontent.com/u/133101799?s=400&u=e9b08cc380e815cf4f929a3f30cb47979d4164f1&v=4" width="115"><br><sub>Ariel Armel Yance Orozco</sub>
</div>
