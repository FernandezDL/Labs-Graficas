# Laboratorio 4 - Shaders II

## Objetivo
El principal objetivo radica en practicar la creación de Shaders en base a _GLSL_, para usarlos en un renderer hecho a base de OpenGL

## Inputs
Debido a que en este programa se pueden hacer inputs a tiempo real, el modelo 3D, y la cámara, pueden sufrir cambios mediante algunas teclas. 

### Movimientos de la cámara
- W: Mueve la cámara hacia arriba
- S: Mueve la cámara hacia abajo
- A: Mueve la cámara hacia la izquierda
- D: Mueve la cámara hacia la derecha
- E: Acerca la cámara hacia el modelo
- Q: Aleja la cámara del modelo

### Cambios de shaders
- 1 - Versión original
  
  Es la versión original del modelo, con la textura que se define en el programa principal y con su forma normal
- 2 - Pie_shader

  Este shader simula ser un Pie de cereza, teniendo sus secciones coloreadas simulando la masa y el relleno
- 3 - Siren_shader

  Este genera un cambio en el color del modelo, haciendo un efecto de transición entre tonos de verde y azul
- 4 - glitch_shader

  Con el glitch_shader se genera un efecto de _falla_, en el cual el modelo se muestra por algunos segundos y desaparece por otro poco de tiempo
- 5 - mixColors_shader

Haciendo definido dos colores, este shader interpola los colores según la coordanada y del pixel correspondiente

### Resultado
El archivo de vídeo correspondiente al resultado del laboratorio está entre los archivos subidos, siendo denominado [Lab4-resultado.mp4](https://drive.google.com/file/d/16I0h6dVNMQkR190nr5snABwsFiYQqr1r/view?usp=drive_link)
