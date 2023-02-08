import pygame,os,time,sys,threading
from button import *
from settingMaze import *
from maze_interface import *

pygame.init()
screen_size=pygame.display.Info()

def settings_Maze(algo_maze,color_mode,n):
    #initialisation de pygame
    pygame.init()
    os.environ['SDL_VIDEO_CENTERED'] = '1'
    #création de la fenêtre
    widht = screen_size.current_w
    height = screen_size.current_h
    screen = pygame.display.set_mode((widht,height),pygame.NOFRAME)

    pygame.mixer.music.load("songs/Motivated.mp3")
    pygame.mixer.music.play()
    pygame.mixer.music.set_volume(0.1)

    res=[10,10]

    boutons = []

    img=pygame.image.load("img/playMaze.png").convert()
    img.set_colorkey((127, 127, 127))
    w,h=img.get_width(),img.get_height()
    x, y = img.get_rect(center=(widht / 2, height / 2.3))[0],img.get_rect(center=(widht / 2, height / 2.3))[1]
    boutons.append(Button("Play", x, y, w, h))

    img = pygame.image.load("img/cross.png").convert()
    img.set_colorkey((127,127,127))
    w,h=img.get_width(),img.get_height()
    x, y = img.get_rect(center=(widht / 1.2, height / 10))[0], img.get_rect(center=(widht / 1.2, height / 10))[1]
    boutons.append(Button("exit", x, y, w, h))

    arrowU = pygame.image.load("img/arrow_up.png").convert()
    w, h = img.get_width(), img.get_height()
    x, y = img.get_rect(center=(widht / 5, height / 4))[0], img.get_rect(center=(widht / 5, height / 4))[1]
    screen.blit(arrowU, [x, y])
    boutons.append(Button("up_widht", x, y, w, h))

    w, h = img.get_width(), img.get_height()
    x, y = img.get_rect(center=(widht / 1.2, height / 4))[0], img.get_rect(center=(widht / 1.2, height / 4))[1]
    screen.blit(arrowU, [x, y])
    boutons.append(Button("up_height", x, y, w, h))

    arrowD = pygame.image.load("img/arrow_down.png").convert()
    w, h = img.get_width(), img.get_height()
    x, y = img.get_rect(center=(widht / 5, height / 2))[0], img.get_rect(center=(widht / 5, height / 2))[1]
    screen.blit(arrowD, [x, y])
    boutons.append(Button("down_widht", x, y, w, h))

    w, h = img.get_width(), img.get_height()
    x, y = img.get_rect(center=(widht / 1.2, height / 2))[0], img.get_rect(center=(widht / 1.2, height / 2))[1]
    screen.blit(arrowD, [x, y])
    boutons.append(Button("down_height", x, y, w, h))

    launched = True

    bg = pygame.image.load("img/bgtest.png").convert()
    bgX = -1
    bgX2 = bg.get_width()
    bgY= -1
    bgY2 = bg.get_height()
    clock = pygame.time.Clock()

    imgs=[pygame.image.load("img/playMaze.png"),pygame.image.load("img/arrow_up.png"),pygame.image.load("img/arrow_down.png")]
    for i in range(len(imgs)):
        w, h = imgs[i].get_width(), imgs[i].get_height()
        new_w, new_h = (w * widht) // 1920, (h * height) // 1080
        imgs[i]=pygame.transform.scale(imgs[i],(new_w,new_h))
        imgs[i].set_colorkey((127,127,127))
    
    imgs_pos=[(widht / 2, height / 2.3),(widht / 5, height / 4),(widht / 1.2, height / 4),(widht / 5, height / 2),(widht / 1.2, height / 2)]
        

    def redrawWindow(pos):

        screen.blit(bg,(bgX,bgY))
        screen.blit(bg,(bgX2,bgY2))

        screen.blit(imgs[0],imgs[0].get_rect(center=imgs_pos[0]))
        screen.blit(imgs[1],imgs[1].get_rect(center=imgs_pos[1]))
        screen.blit(imgs[1],imgs[1].get_rect(center=imgs_pos[2]))
        screen.blit(imgs[2],imgs[2].get_rect(center=imgs_pos[3]))
        screen.blit(imgs[2],imgs[2].get_rect(center=imgs_pos[4]))

        img = pygame.image.load("img/cross.png")
        img.set_colorkey((127,127,127))
        x, y = img.get_rect(center=(widht/1.2, height/10))[0],img.get_rect(center=(widht/1.2, height/10))[1]
        screen.blit(img,(x,y))
        
        font_size = (35 * widht) // 1920
        widht_txt = pygame.font.Font('Estelle.ttf', font_size).render("Largeur : " + str(res[0]), True, (res[0]*2,res[1]*2, int((res[0]/res[1])*3)))
        rect = pygame.Rect(widht_txt.get_rect(center=(widht / 5, height / 2.6))[0],widht_txt.get_rect(center=(widht / 1.2, height / 2.6))[1], widht_txt.get_width(),widht_txt.get_height())
        pygame.draw.rect(screen, (255, 255, 255), rect)
        screen.blit(widht_txt, widht_txt.get_rect(center=(widht/5, height/2.6)))

        height_txt = pygame.font.Font('Estelle.ttf',font_size).render("Hauteur : " + str(res[1]), True, (res[1]*2, res[0]*2, int((res[1]/res[0])*3)))
        rect=pygame.Rect(height_txt.get_rect(center=(widht/1.2, height/2.6))[0],height_txt.get_rect(center=(widht/1.2, height/2.6))[1],height_txt.get_width(),height_txt.get_height())
        pygame.draw.rect(screen,(255,255,255),rect)
        screen.blit(height_txt, height_txt.get_rect(center=(widht/1.2, height/2.6)))

        font_size = (20 * widht) // 1920
        authors = pygame.font.Font('Estelle.ttf', font_size).render("Crée par : LAVOILLOTTE Ethan et WEBER Loïc", True, (0, 255, 0))
        rect = pygame.Rect(authors.get_rect(center=(widht / 1.2, height / 1.2))[0],
                           authors.get_rect(center=(widht / 1.3, height / 1.1))[1],
                           authors.get_width(), authors.get_height())
        pygame.draw.rect(screen, (0, 0, 0), rect)
        screen.blit(authors, authors.get_rect(center=(widht / 1.2, height / 1.1)))

        pygame.display.update()

    speed=60

    while launched:
        try:
            pos = pygame.mouse.get_pos()
            redrawWindow(pos)
            clock.tick(speed)
            bgX-=1.75
            bgX2-=1.75
            bgY-=1.25
            bgY2-=1.25
            if bgX<bg.get_width()*-1:
                bgX=bg.get_width()
            if bgX2<bg.get_width()*-1:
                bgX=bg.get_width()
            if bgY<bg.get_height()*-1:
                bgY=bg.get_height()
            if bgY2<bg.get_height()*-1:
                bgY=bg.get_height()

            if bgX>=7000 and bgX2<-7000 and bgY>=5000 and bgY2<=-5000:
                bgX=-217
                bgX2=bg.get_width()
                bgY=-217
                bgY2=bg.get_height()
        except:pass

        for event in pygame.event.get():

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                for bouton in boutons:
                    if bouton.isOver(pos) :
                        if bouton.name=="exit":launched=False
                        elif bouton.name =="up_widht" and res[0]<80:res[0]+=1
                        elif bouton.name=="up_height" and res[1]<54:res[1]+=1
                        elif bouton.name=="down_widht" and res[0]>1:res[0]-=1
                        elif bouton.name=="down_height" and res[1]>1:res[1]-=1
                        elif bouton.name=="Play":
                            maze_interface = new_window("Tuto", screen_size, res[0], res[1], 0, 0, 0, "Tuto",algo_maze,color_mode,n)
                            maze_interface.launch_loop()
            if event.type == pygame.QUIT:
                launched = False

        pygame.display.flip()
