# Python3 code to draw a triangle and find centroid

# importing libraries
import numpy as np
import cv2
from imageShape import *

if __name__ == '__main__':

    #El usuario ingresa el valor del ancho y alto de la imagen
    width = int(input('Ingrese el ancho de la imagen: '))
    height = int(input('Ingrese el alto de la imagen: '))

    #Se inicializa la class imageShape
    img = imageShape(width, height)

    #Se realizan los métodos
    img.generateShape()                      #Genera la figura aleatoria
    img.showShape()                          #Muestra la imagen durante 5 segundos
    name, image = img.getShape()             #Retorna la imagen y el nombre teórico de la figura
    objeto=img.whatShape(image)              #Se ingresa la figura que se quiere detectar y retorna el nombre
    print('La figura teórica es:',name )     #Nombre teórico
    print('La figura detectada es:',objeto)  #Nombre detectado