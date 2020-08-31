#importar librerias necesarias
import numpy as np
import cv2
import math
from numpy.random import seed
from numpy.random import randint
from heapq import nsmallest

class imageShape:

    #Constructor, entradas ancho y alto
    def __init__(self, width, height):
        self.width = width
        self.height = height

    #Método generateShape
    def generateShape(self):
        #Matriz de ceros para generar la imagen negra
        self.shape = np.zeros((self.height, self.width, 3),np.uint8)
        # generar un número aleatorio entre 0 y 3
        self.k = randint(0,3,1)

        #Dependiendo del valor generado aleatoriamente se ingresa a alguna de las opciones
        #Si es 0, se hace un triángulo
        if self.k == 0:
            #Valores necesarios para hallar los puntos de los vértices del triangulo, como el valor del lado y la altura
            lado_tiangle = int(min(self.width, self.height) / 2)
            altura = int(math.sqrt((lado_tiangle ** 2) - ((lado_tiangle / 2) ** 2)))

            #Valor en x y y de los tres puntos teniendo en cuenta el centro como el centro de la imagen
            point1_x = int(self.width / 2)
            point1_y = int((self.height / 2) - ((2 * altura) / 3))
            point2_x = int((self.width / 2) + (lado_tiangle / 2))
            point2_y = int((self.height / 2) + (altura / 3))
            point3_x = int((self.width / 2) - (lado_tiangle / 2))
            point3_y = int((self.height / 2) + (altura / 3))

            #Concatenan los puntos
            points = np.array(
                [[point1_x, point1_y], [point2_x, point2_y], [point3_x, point3_y]],
                np.int32)

            #Se dibuja el contorno sobre la imagen negra y rellenando con colo cyan (azul y verde)
            cv2.drawContours(self.shape, [points], 0, (255, 255, 0), -1)

        #Si es 1, se hace un cuadrado
        if self.k == 1:
            #Valor del lado para hallar los vertices del cuadrado
            lado_square = min(self.width, self.height) / 2

            #Valor en x y y de los dos puntos contrarios teniendo en cuenta el centro como el centro de la imagen
            point1_x = int((self.width / 2) + (lado_square/2))
            point1_y = int((self.height / 2) + (lado_square / 2))
            point2_x = int((self.width / 2) - (lado_square/2))
            point2_y = int((self.height / 2) - (lado_square / 2))

            #Se genera el cuadrado con color cyan
            cv2.rectangle(self.shape, (point1_x, point1_y), (point2_x, point2_y), (255, 255, 0), -1)

            #Se rota la imagen creada 45 grados
            M =  cv2.getRotationMatrix2D((self.width//2,self.height//2),45,1)
            self.shape = cv2.warpAffine(self.shape, M, (self.width, self.height))

        # Si es 1, se hace un cuadrado
        if self.k == 2:
            # Valor del lado horizontal y el lado vertical para hallar los vertices del rectangulo
            lado_horizontal = self.width//2
            lado_vertical = self.height//2

            # Valor en x y y de los dos puntos contrarios teniendo en cuenta el centro como el centro de la imagen
            point1_x = int((self.width / 2) + (lado_horizontal / 2))
            point1_y = int((self.height / 2) + (lado_vertical / 2))
            point2_x = int((self.width / 2) - (lado_horizontal / 2))
            point2_y = int((self.height / 2) - (lado_vertical / 2))

            # Se genera el rectángulo con color cyan
            cv2.rectangle(self.shape, (point1_x, point1_y), (point2_x, point2_y), (255, 255, 0), -1)

        # Si es 1, se hace un circulo
        if self.k == 3:
            # Valor del radio y el centro para dibujar el circulo
            radio = min(self.width, self.height) // 4
            center_x = self.width // 2
            center_y = self.height // 2

            # Se genera el circulo con color cyan
            cv2.circle(self.shape, (center_x, center_y), radio, (255, 255, 0), -1)

    # Método showShape
    def showShape(self):
        #Se visualiza la imagen generada en generateShape por 5 segundos
        cv2.imshow('base', self.shape)
        cv2.waitKey(5000)

    # Método getShape
    def getShape(self):
        #Dependiendo de la imagen generada segun el valor de k se guarda el string del nombre
        if self.k == 0:
            self.name = 'Triangle'
        if self.k == 1:
            self.name = 'Square'
        if self.k == 2:
            self.name = 'Rectangle'
        if self.k == 3:
            self.name = 'Circle'

        #Retorna la imagen y el nombre
        return self.name, self.shape

    # Método whatShape
    def whatShape(self, image):
        #Entra la imagen a identificar la figura y se hace una copia
        self.image = image
        image_draw = self.image.copy()

        #Se encuenta el contorno de la imagen
        #Para esto se pasa la imagen a escala de grises
        image_gray = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
        #Se halla el umbral y el contorno con las funciones
        ret, thresh = cv2.threshold(image_gray, 127, 255, 0)
        contours, hierarchy = cv2.findContours(thresh, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

        #Se hallan los momentos, que me da la información del area de la figura en M['m00']
        M = cv2.moments(contours[0])
        area = M['m00']

        #Se hallan los valores teóricos de cada figura según el ancho y alto ingresado
        #Triángulo
        altura = math.sqrt(((min(self.width, self.height) / 2) ** 2) - (((min(self.width, self.height) / 2) / 2) ** 2))
        area_triangle = (altura*((min(self.width, self.height) / 2)))/2
        #Cuadrado
        area_square = (min(self.width, self.height)/2)**2
        #Rectángulo
        area_rectangle = (self.width/2)*(self.height/2)
        #Circulo
        radio = min(self.width, self.height) / 4
        area_circle = math.pi * (radio**2)

        #Se concatenan los valores hallados
        areas = [area_triangle,area_square,area_rectangle,area_circle]

        #Se halla el valor teórico que este más cercano al área hallada de la figura
        figura = nsmallest(1, areas, key=lambda x: abs(x-area))

        # Se guardan las variables para poder compararlas
        area1 = [area_triangle]
        area2 = [area_square]
        area3 = [area_rectangle]
        area4 = [area_circle]

        #Se comparan los resultados, así definir que tipo de figura es
        if figura == area1:
            self.name = 'Triangle'
        elif figura == area2:
            self.name = 'Square'
        elif figura == area3:
            self.name = 'Rectangle'
        elif figura == area4:
            self.name = 'Circle'
        else:
            self.name = 'none'

        #Se retorna el nombre de la figura detectada
        return self.name