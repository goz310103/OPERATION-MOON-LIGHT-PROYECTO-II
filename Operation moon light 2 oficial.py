#Operation moon light
from QuickSort import *
import pygame, sys, random, vlc
from pygame import mixer
from pygame.locals import *

# Inicio el juego.
pygame.init()

# Defino el control de audio del juego, esta es una función de pygame que permite establecer las frecuencias, canales,
# profundidad de bits y el buffer del audio que vamos a reproducir, los valores los están asignado por defecto.
pygame.mixer.pre_init(44100, -16, 2, 512)
mixer.init()

# De una vez pongo a correr la mùsica principal y la voy parando cada vez que entra a un nivel
menu_principal = vlc.MediaPlayer("canciones\pantallainicio.mp3")
nivel_1 = vlc.MediaPlayer("canciones/nivel1.mp3")
nivel_2 = vlc.MediaPlayer("canciones/nivel2.mp3")
nivel_3 = vlc.MediaPlayer("canciones/nivel3.mp3")

# Cargo los efectos de sonido a una variable y les reducí el sonido a un volumen agradable.
explosion1_efecto = pygame.mixer.Sound(f"efectos\explosion2.mp3")
explosion1_efecto.set_volume(0.25)
explosion2_efecto = pygame.mixer.Sound(f"efectos\explosion2.mp3")
explosion2_efecto.set_volume(0.25)
contacto_efecto = pygame.mixer.Sound(f"efectos\contacto1.mp3")
contacto_efecto.set_volume(0.25)
contacto2_efecto = pygame.mixer.Sound(f"efectos\contacto2.mp3")
contacto2_efecto.set_volume(0.25)


def colision(x):
    pared_efecto = pygame.mixer.Sound(f"efectos\p" + str(x) + ".wav")
    pared_efecto.set_volume(0.16)
    pared_efecto.play()


# Defino la velocidad de actualizacion de la ventana, pygame.time.Clock() me crea una especie de objeto o reloj que limita los cuadros por segundo de actualización de la ventana al numero que se le ingrese.
# Mi variable fps significa fotogramas por segundo y luego va ser la encargada de limitar el anteriormente mencionado Clock a 60 fotogramas por segundo.
actualizacion = pygame.time.Clock()
fps = 60
niveles = False

# Defino la ventana, creo un ancho y un alto para luego crear una variable llamada ventana, la cual con la función pygame.display.set_mode se convierte en una ventana de pygame
ventana_ancho = 600
ventana_alto = 800
ventana = pygame.display.set_mode((ventana_ancho, ventana_alto))
# Con pygame.display.set_caption le asigno un nombre a la barra superior de la ventana anteriormente creada.
pygame.display.set_caption("Operation Moon Light")

# A las siguientes variables les asigné una imagen la cual luego voy a estar utilizando para pintar el fondo de las diferentes pantallas.
fondo = pygame.image.load("img\pondo.jpg")
fondo_complementaria = pygame.image.load("img\pondo_comp.jpg")
fondo_puntajes = pygame.image.load("img\pondo_punt.jpg")

# Las siguientes variables corresponden a textos en forma de imagen que luego estaré utilizando para pintarlas de en pantalla de manera que queden como títulos.
titulo = pygame.image.load("img\ditulos\ditulo.png")
titulo_comp = pygame.image.load("img\ditulos\dituloi.png")
titulo_punt = pygame.image.load("img\ditulos\ditulop.png")

# En las siguientes variables defino unas fuentes que luego voy a utilizar. La variable pygame.font.Font hace referencia a retornar una fuente de letra con un tamaño asignable.
fuente_base = pygame.font.Font(None, 32)
fuente20 = pygame.font.SysFont("Rockwell", 20)
fuente30 = pygame.font.SysFont("Constantia", 30)
fuente40 = pygame.font.SysFont("Rockwell", 40)


# Estas funciones son las que se encargan de pintar el fondo y los titulos una vez que la funcion sea llamada.
def dibujar_fondo_p(x):
    fondolvl = pygame.image.load("img/pondos/principal/frame_" + str(x) + "_delay-0.04s.gif")
    ventana.blit(fondolvl, (0, 0))


def dibujar_fondo2():
    ventana.blit(fondo_complementaria, (0, 0))


def dibujar_fondo3():
    ventana.blit(fondo_puntajes, (0, 0))


def dibujar_titulo():
    ventana.blit(titulo, (ventana_ancho / 2 - 128, 10))


def dibujar_titulo_comp():
    ventana.blit(titulo_comp, (ventana_ancho / 2 - 150, 20))


def dibujar_titulo_punt():
    ventana.blit(titulo_punt, (ventana_ancho / 2 - 122, 20))


def dibujar_lvl1(x):
    fondolvl = pygame.image.load("img/pondos/pondolvl1/" + str(x) + ".gif")
    ventana.blit(fondolvl, (0, 0))


def dibujar_lvl2(x):
    fondolvl = pygame.image.load("img/pondos/pondolvl2/frame_" + str(x) + "_delay-0.03s.gif")
    ventana.blit(fondolvl, (0, 0))


def dibujar_lvl3(x):
    fondolvl = pygame.image.load("img/pondos/pondolvl3/frame_" + str(x) + "_delay-0.04s.gif")
    ventana.blit(fondolvl, (0, 0))


# A las siguiente variables les asigne un color el cual hace referencia al nombre de la variable.
rojo = (255, 0, 0)
verde = (0, 255, 0)
blanco = (255, 255, 255)
amarillo_verde = (150, 255, 0)
amarillo = (255, 220, 0)
rojo_amarillento = (255, 120, 0)


# La siguiente función me permite que al ser llamada e inicioduciendole el texto que yo quiera, la fuente y la posición, este mismo sea añadido a la pantalla en forma de imagen.
# Gracias a la función de pygame.blit puedo añadir a mi ventana la imagen que yo le asigne.
def dibujar_texto(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    ventana.blit(img, (x, y))


# A continuación defino una clase para el jugador1, basado en un sprite, en la cual le asigno la posición inicial y la vida.
class Jugador1(pygame.sprite.Sprite):
    def __init__(self, x, y, vida):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("img/player.png")
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.vida_inicio = vida
        self.vida_restante = vida
        self.score = 0
        self.nombre = ""
        self.posición = 1

    # La siguiente función se encarga de actualizar la posición y la vida del jugador1 por cada fotograma. (Fotogramas asignados por Clock)
    def update(self):
        if self.score < 0:
            self.score = 0
        # Defino una variable con la velocidad de movimiento a la que quiero que mi personaje se mueva y otra variable llamada fin_del_juego, la cual se encargará luego de manterner el Nivel 1 corriendo.
        velocidad = 8
        fin_del_juego = 0

        # A continuación defino que las teclas de movimiento "flechas" y "wasd" muevan al personaje al ser presionadas, esto al sumarle a la posición (en x o en y) la velocidad que asigné anteriormente. (Decicí añadir las telcas de movimiento wasd dado que resulta más cómodo y eficiente, además quería darle un "easteregg" ya que si utilizas las flechas y wasd tu velocidad será el doble)
        # La función pygame.get_pressed[x] me retorna si x tecla está siendo presionada. Con lo cual tome esta función y la iniciofuje en una variable llamada tecla.
        tecla = pygame.key.get_pressed()
        # A continuación utiliza la variable tecla asignandola a cada tecla de movimiento, para que si dicha tecla es presionada le sume o reste (en x o y) la velocidad de movimiento a la posición del jugador #1
        # además para que esto se de, se debe cumplir que la posición del personaje esté en el rango de la pantalla, para evitar así que este se salga de la misma.
        if tecla[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= velocidad
        if tecla[pygame.K_RIGHT] and self.rect.right < ventana_ancho:
            self.rect.x += velocidad
        if tecla[pygame.K_UP] and self.rect.top > 0:
            self.rect.y -= velocidad
        if tecla[pygame.K_DOWN] and self.rect.bottom < ventana_alto - 50:
            self.rect.y += velocidad
        # También quise asignar las teclas de movimiento a "wasd"
        if tecla[pygame.K_a] and self.rect.left > 0:
            self.rect.x -= velocidad
        if tecla[pygame.K_d] and self.rect.right < ventana_ancho:
            self.rect.x += velocidad
        if tecla[pygame.K_w] and self.rect.top > 0:
            self.rect.y -= velocidad
        if tecla[pygame.K_s] and self.rect.bottom < ventana_alto - 50:
            self.rect.y += velocidad
        # Creo una máscara de los pixeles de la nave, esta mascara me crea una forma igual a la imagen de mi nave, forma que luego utilizaré para las colisiones, de esta manera aunque mi imagen tenga unas dimensiones
        # si la bala enemiga no entra en contacto con los pixeles pintados de la imagen, esta no causa daño, así logro que la bala de verdad colisione con mi nave cuando debe.
        self.mask = pygame.mask.from_surface(self.image)

        # A continuación defino la vida del jugador #1 de panera que si esta es mayor a 0 aparezca en pantalla y retorno que fin del juego = 0 (o sea que el juego aún no termina), si no,
        # en el momento que la vida sea menor o igual a 0 añado una animación de explosión a mi nave, reproduzco un sonido de explosión y retorno fin del juego = -1, lo que quiere decir que perdió.
        if self.vida_restante > 0:
            dibujar_texto("Vida: " + str(self.vida_restante), fuente30, verde, int(ventana_alto / 2 - 40), int(760))
            dibujar_texto(str(self.nombre), fuente30, verde, int(ventana_alto / 2 - 210), int(760))
        elif self.vida_restante <= 0:
            exp = Explosion2(self.rect.centerx, self.rect.centery)
            explosion_group.add(exp)
            explosion1_efecto.play()
            fin_del_juego = -1

        return fin_del_juego


# Defino la animación de explosión como una clase basada en un sprite.
class Explosion(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        # Defino una lista que me servirá para imprimir cada elemento de la lista, de manera que añadiendo cada imagen a la lista, esta se imprima luego de la anterior, dando el efecto animado.
        self.imagenes = []
        # A continuación simplemente le asigno una variable a cada imagen de la animación. (Imagenes de la animación tomadas de Coding With Russ)
        img1 = pygame.image.load(f"img\Animaciones\exp1.png")
        img2 = pygame.image.load(f"img\Animaciones\exp2.png")
        img3 = pygame.image.load(f"img\Animaciones\exp3.png")
        img4 = pygame.image.load(f"img\Animaciones\exp4.png")
        img5 = pygame.image.load(f"img\Animaciones\exp5.png")
        # Añado cada imagen a la lista de la animación
        self.imagenes.append(img1)
        self.imagenes.append(img2)
        self.imagenes.append(img3)
        self.imagenes.append(img4)
        self.imagenes.append(img5)
        # Defino un indice que irá cambiando, y este será quien defina que imagen dibujar en pantalla.
        self.indice = 0
        # Defino una variable imagen la cual es igual a la imagen que se encuentra en la posición del indice, índice que luego al actualizarse va a ir cambiando.
        self.image = self.imagenes[self.indice]
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        # Este contador se va encargar de controlar la velocidad a la que cambia la imagen que se este dibujando en ese momento.(imagen del grupo de imagenes de la explosión)
        self.contador = 0

    def update(self):
        # Defino una variable que me ayudara a controlar la velocidad de la animación.
        velocidad_explosion = 4
        # Le sumo 1 al contador de manera que en algun momento este sea mayor a la velocidad, y cada vez que esto pase se va a pintar una imagen diferente.
        self.contador += 1
        if self.contador >= velocidad_explosion and self.indice < len(self.imagenes) - 1:
            self.contador = 0
            self.indice += 1
            self.image = self.imagenes[self.indice]

        # Cuando la animación se completa, eliminamos la animación de explosión.
        if self.indice >= len(self.imagenes) - 1 and self.contador >= velocidad_explosion:
            self.kill()


# A continuación hice exactamente lo mismo pero con imagenes de explosión más grandes, esto debido a que podría haberlo hecho en una sola clase pero no se por qué motivo pygame no me detectaba la funcion pygame.transform.scale
class Explosion2(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.imagenes = []
        img1 = pygame.image.load(f"img\Animaciones\expg1.png")
        img2 = pygame.image.load(f"img\Animaciones\expg2.png")
        img3 = pygame.image.load(f"img\Animaciones\expg3.png")
        img4 = pygame.image.load(f"img\Animaciones\expg4.png")
        img5 = pygame.image.load(f"img\Animaciones\expg5.png")
        # Añado la imagen a la lista de la animación
        self.imagenes.append(img1)
        self.imagenes.append(img2)
        self.imagenes.append(img3)
        self.imagenes.append(img4)
        self.imagenes.append(img5)
        self.indice = 0
        self.image = self.imagenes[self.indice]
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.contador = 0

    def update(self):
        velocidad_explosion = 4
        # Cambio la velocidad de la animación
        self.contador += 1

        if self.contador >= velocidad_explosion and self.indice < len(self.imagenes) - 1:
            self.contador = 0
            self.indice += 1
            self.image = self.imagenes[self.indice]

        # Cuando la animación se completa, eliminamos la explosión
        if self.indice >= len(self.imagenes) - 1 and self.contador >= velocidad_explosion:
            self.kill()


# En la siguiente clase defino los botones, de manera que estos tengan 2 imagenes, una cuando el mouse está sobre ellos y otra cuando el mouse no lo está.
class Boton(pygame.sprite.Sprite):
    def __init__(self, imagen1, imagen2, x=ventana_ancho / 2 - 15, y=ventana_alto / 2 - 200):
        self.imagen_normal = imagen1
        self.imagen_seleccion = imagen2
        self.imagen_actual = self.imagen_normal
        self.rect = self.imagen_actual.get_rect()
        self.rect.left, self.rect.top = (x, y)

    def update(self, ventana, cursor):

        if cursor.colliderect(self.rect):
            self.imagen_actual = self.imagen_seleccion
        else:
            self.imagen_actual = self.imagen_normal
        ventana.blit(self.imagen_actual, self.rect)
