import pygame
from threading import Thread
import unicodedata
import pygame.camera
import sys as r
import traceback
import ctypes  # An included library with Python install.


def Mbox(title, text, style):
    return ctypes.windll.user32.MessageBoxW(0, text, title, style)


def CEMB(text):
    return ctypes.windll.user32.MessageBoxW(0, text, "An exception occured", 16)


"""

try:
    raise ValueError
except ValueError:
    tb = traceback.format_exc()
else:
    tb = "No error"
finally:
    ##print tb
    """
import os


def rcc(s):
    return "".join(ch for ch in s if unicodedata.category(ch)[0] != "C")


############################################# fonts
FONT_SIZE = 20
pygame.font.init()
# font = pygame.font.Font('engine/fonts/main.ttf', FONT_SIZE)
font = pygame.font.SysFont("@MS Gothic", FONT_SIZE)

titlefont = pygame.font.SysFont("@MS Gothic", 30)  # pygame.font.SysFont('Consolas', 30)
menufont = pygame.font.SysFont("@MS Gothic", 24)  # pygame.font.SysFont('Consolas', 24)
mainfont = pygame.font.SysFont("@MS Gothic", 24)  # pygame.font.SysFont('Arial', 24)


class InputField:
    def __init__(self, screen: pygame.display) -> None:
        self.fields = dict()
        self.screen = screen

    def addField(self, field: pygame.Rect, iid: int):
        self.fields[iid] = {"field": field, "input": "", "active": False}

    def displayField(self, iid: int, color: tuple, seccolor=(0, 0, 0)):
        f = self.fields[iid]["field"]
        s = self.fields[iid]["input"]
        if s == "":
            s = "empty"
            seccolor = (seccolor[0] + 80, seccolor[1] + 80, seccolor[2] + 80)
        nacolor = (color[0] - 40, color[0] - 40, color[0] - 40)
        if self.fields[iid]["active"]:
            pygame.draw.rect(self.screen, color, f)
        else:
            pygame.draw.rect(self.screen, nacolor, f)
        text_surface = mainfont.render(s, True, seccolor)
        screen.blit(text_surface, f)

    def addChrToField(self, iid: int, s: str):
        if self.fields[iid]["active"]:
            self.fields[iid]["input"] += s
        else:
            pass  # #print(f"tried to add a char to non-active field, see {self.fields[iid]}",1)

    def delChrFromField(self, iid: int):
        if self.fields[iid]["active"]:
            self.fields[iid]["input"] = self.fields[iid]["input"][:-1]
        else:
            pass  # #print(f"tried to del a char to non-active field, see {self.fields[iid]}",1)

    def getInputFromField(self, iid: int):
        return self.fields[iid]["input"]

    def setActiveField(self, iid: int):  # only one field could be active
        for field in self.fields:
            if iid != field:
                self.fields[field]["active"] = False
        self.fields[iid]["active"] ^= 1

    def deActivateField(self, iid: int):
        self.fields[iid]["active"] = False


pygame.init()
screen = pygame.display.set_mode((800, 550), pygame.ASYNCBLIT)
commands = InputField(screen)

clock = pygame.time.Clock()
FPS = 60
version = [1, 4]
text = []
script = []
strv = ".".join(list(map(str, version)))
running = True


cursor = pygame.image.load("engine/decals/dwarf_cursor.png")

# #print("@ipebyx и @prostopelmenhto представляют")
# #print(f"БЕГИ ЗА АНАНАСОМ!, v{strv}")
name = "Беги за ананасом!"
pygame.display.set_caption(name)
pygame.display.set_icon(pygame.image.load("engine/decals/dwarf_missing.png"))
g = 0
creatorMode = False

modesforreal = ["decal", "hitbox", "leveltrigger"]
modesforcounter = 1
zimagelayer = {}
modes = "hitbox"


def resetgamestates():
    global mc
    mc = []
    global debugRectInfo
    debugRectInfo = []
    global zimagelayer
    zimagelayer = {}
    global text
    text = []
    global triggers
    triggers = []
    global debugTexInfo
    debugTexInfo = []
    global debilsize
    debilsize = [22, 22]
    global debilspid
    debilspid = [0, 0]
    global remove
    remove = False
    global removeDecals
    removeDecals = False
    global camsomewhere
    camsomewhere = []
    global platformo
    platformo = []
    global debilcoords
    debilcoords = [0, 0]
    global cameraposition
    cameraposition = [0, 0]
    global decals
    decals = []
    global textures
    textures = []
    global levelplatformo
    levelplatformo = []
    global author
    author = ""
    global description
    description = ""
    global title
    title = ""
    global fillercolor
    fillercolor = (0, 0, 0)


resetgamestates()


def ImageInit(silent=True):
    global decals
    global textures

    for dec in decals:
        # #print(dec)
        try:
            image = pygame.image.load(dec[0])
        except:
            if not silent:
                CEMB(
                    f'ТЕКСТУРА "{dec[0]}" НЕ НАЙДЕНА /\nTEXTURE "{dec[0]}" IS NOT FOUND'
                )
            # #print(f'ТЕКСТУРА "{dec[0]}" НЕ НАЙДЕНА')
            # raise FileNotFoundError(f'ТЕКСТУРА "{dec[0]}" НЕ НАЙДЕНА')
            image = pygame.image.load("engine/decals/dwarf_missing.png")
        image = image.convert_alpha()
        transparency = int(dec[2])
        image.set_alpha(transparency)
        position = dec[1]
        textures.append(
            {
                "image": image,
                "transparency": transparency,
                "position": position,
                "name": dec[0],
            }
        )
        ###print({"image":image,"transparency":transparency,"position":position,"name":dec[0]})
        # link, [posx, posy], transparency


######## ACTUAL SHIT
def load_level(file):
    resetgamestates()
    k = open(file)
    m = k.readlines()
    k.close()
    global SNAP
    global DIV
    global hitboxes
    global images
    global decals
    global linking
    global campos
    global plrspwn
    global zimagelayer
    global camsp
    global fillercolor
    global author
    global title
    global desc
    global debilcoords
    global cameraposition
    global color
    global ver
    global linking
    global decals
    global script
    global text
    global triggers
    global r
    global b
    global g

    SNAP = 15
    DIV = 1
    script = []
    text = []
    triggers = []
    zimagelayer = {}
    hitboxes = []
    images = []
    decals = []
    linking = []
    campos = [0, 0]
    decalcounter=0
    for line in m:

        sl = line.split(" ", 1)
        sh = sl[1]
        if sl[0] == ".IP":
            x, y = list(map(int, sl[1].split(",")))
            debilcoords = [x, y]
            # #print(f'player spawn at {x=},{y=}')
            # #print(debilcoords)
        if sl[0] == ".ICP":
            x, y = list(map(int, sl[1].split(",")))
            cameraposition = [x, y]
            # #print(f'camera spawn at {x=},{y=}')
        if sl[0] == ".A":
            st = sl[1].split(",")[-1].strip()
            author = st
            # #print(f'author: {st}')
        if sl[0] == ".T":
            st = sl[1].split(",")[-1].strip()
            title = st
            # #print(f'title: {st}')
        if sl[0] == ".F":
            r, g, b = list(map(int, sl[1].split(",")))
            fillercolor = (r, g, b)
            # #print(f'filler color: {r=},{g=},{b=}')
        if sl[0] == ".DV":
            st = sl[1].split(",")[-1].strip()
            # #print(f'version: {st}')
            ver = st
        if sl[0] == "H":
            x, y, w, h = list(map(int, sl[1].split(",")))
            # #print(f'hitbox at {x=},{y=} with {w=},{h=}')
            platformo.append(pygame.Rect(x, y, w, h))
        if sl[0] == "L":
            x, y, w, h = list(map(int, sl[1].split(",")[0:4]))
            l = sl[1].split(",")[4].strip()
            # #print(f'linking hitbox at {x=},{y=} with {w=},{h=} linking to {l=}')
            linking.append([pygame.Rect(x, y, w, h), l])
        if sl[0] == "I":

            x, y, l, t = (
                int(sh.split(",")[0]),
                int(sh.split(",")[1]),
                sh.split(",")[2].strip(),
                int(sh.split(",")[3]),
            )

            try:
                z=int(sh.split(",")[4].strip())
                try:
                    #print(zimagelayer)
                    zimagelayer[z].append(decalcounter)
                except Exception as asdasdasd:
                    zimagelayer[z]=[decalcounter]
                #print(f'found image w/ z layer technology, {z=}')
            except IndexError as r:
                #print(f'{r}\n---\nplease keep in mind that THIS decal will show behind every decal with Z layer eg. z layer =-99\nEOE---')
                try:
                    zimagelayer[-99].append(decalcounter)
                except:
                    zimagelayer[-99]=[decalcounter]
                
            #print(f"image at {x=},{y=} linking to {l} w/ transparency {t}")
            decalcounter+=1
            decals.append([l, [x, y], t])
        if sl[0] == "T":

            x, y, r, g, b, t = (
                int(sh.split(",", 5)[0]),
                int(sh.split(",", 5)[1]),
                int(sh.split(",", 5)[2]),
                int(sh.split(",", 5)[3]),
                int(sh.split(",", 5)[4]),
                sh.split(",", 5)[5:][0].strip(),
            )
            text.append([x, y, r, g, b, t])
        if sl[0] == "R":

            #print(list(map(int, sh.split(",")[:-1])))
            #print(int(sh.split(",")[-1]))
            id = int(sh.split(",")[-1])
            x, y, w, h = list(map(int, sh.split(",")[:-1]))
            triggers.append([x, y, w, h, id])
            #print(f"trigger at {x=},{y=} with {w=},{h=} w/ {id=}")
        if sl[0] == "S":
            script.append(sh.strip())

            #print(f"script w/ name {sh.strip()}")
    ImageInit()
    #print()


def displaytext(text, pos, transparency=255, color=(0, 0, 1)):  ## DEBUGG

    if color == (0, 0, 1):
        color = (255 - color[0], 255 - color[1], 255 - color[2])
    text = font.render(text, True, color).convert_alpha()
    text.set_alpha(transparency)
    screen.blit(text, pos)


"""
try:
    basename=r.argv[1]
except:
    basename=input("karta name? ")
"""
commands.addField(pygame.Rect(10, 10, 780, 32), 2)  ## map name
commands.setActiveField(2)
basename = ""
n = os.listdir("maps/")
versions = {}
for m in n:
    try:
        load_level(m, False)
        if len(title[0:7]) < len(title):
            versions[
                m
            ] = f"{strv} | {title[0:7]}... by {author[0:10].replace('unknown','???')}"
        elif title == "":
            versions[m] = f"{strv} | ??? by {author[0:10].replace('unknown','???')}"
        else:
            versions[m] = f"{strv} | {title} by {author[0:10].replace('unknown','???')}"
    except Exception as e:
        # #print(e)
        versions[m] = "FAIL"

import datetime
import time


def size_dir(d):
    file_walker = (
        os.path.join(root, f) for root, _, files in os.walk(d) for f in files
    )
    return sum(os.path.getsize(f) for f in file_walker)


import shutil


def check_things():
    CHECKINGDIR = True
    # #print(commands.fields)
    while CHECKINGDIR:
        clock.tick()
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if commands.fields[2]["active"] and event.type == pygame.KEYDOWN:
                kp = pygame.key.name(event.key)
                kp = rcc(kp)
                if kp == "backspace":
                    commands.delChrFromField(2)
                elif (
                    not kp == "return"
                    and not kp == "left ctrl"
                    and not kp == "right ctrl"
                    and not kp == "escape"
                ):
                    commands.addChrToField(2, event.unicode.replace(chr(127), ""))
                elif kp == "return":
                    basename = commands.fields[2]["input"]
                    if basename.split()[0] == "pack":
                        shutil.make_archive(
                            "maps/" + basename.split()[1],
                            "zip",
                            "maps/" + basename.split()[1],
                        )
                        basename.split()[0] = ""
                        check_things()

                        CHECKINGDIR = False
                    commands.deActivateField(2)
                    CHECKINGDIR ^= 1
        screen.fill((0, 0, 0))
        pygame.draw.rect(screen, (32, 32, 32), pygame.Rect(10, 50, 780, 800))
        co = 0
        for l in n:
            l = l.replace("pack ", "")
            displaytext("Name", [20, 60], 255, color=(0, 255, 255))
            displaytext("Size", [120, 60], 255, color=(0, 255, 255))
            displaytext("Created at", [220, 60], 255, color=(0, 255, 255))
            displaytext("Changed at", [380, 60], 255, color=(0, 255, 255))
            displaytext("Info", [520, 60], 255, color=(0, 255, 255))

            size = size_dir("maps/" + l)
            try:
                date = os.stat("maps/" + l + "/main").st_ctime
                date2 = os.stat("maps/" + l + "/main").st_mtime

            except Exception as e:
                date = 0
                date2 = 0
            if commands.fields[2]["input"] == l:
                displaytext(
                    versions[l], [520, 90 + co * FONT_SIZE], 255, color=(200, 200, 200)
                )
                displaytext(l[0:10], [20, 90 + co * FONT_SIZE], 255, color=(0, 255, 0))
                displaytext(
                    f"{size}b", [120, 90 + co * FONT_SIZE], 255, color=(128, 255, 128)
                )
                if date != 0:
                    displaytext(
                        f"{datetime.date.fromtimestamp(date)}",
                        [220, 90 + co * FONT_SIZE],
                        255,
                        color=(128, 255, 128),
                    )
                    displaytext(
                        f"{datetime.date.fromtimestamp(date2)}",
                        [380, 90 + co * FONT_SIZE],
                        255,
                        color=(128, 255, 128),
                    )
                else:
                    displaytext(
                        f"{datetime.date.fromtimestamp(date)}",
                        [220, 90 + co * FONT_SIZE],
                        255,
                        color=(128, 255, 128),
                    )
                    displaytext(
                        f"{datetime.date.fromtimestamp(date2)}",
                        [380, 90 + co * FONT_SIZE],
                        255,
                        color=(128, 255, 128),
                    )
                co += 0.8
            elif commands.fields[2]["input"] in l:
                displaytext(
                    versions[l], [520, 90 + co * FONT_SIZE], 255, color=(200, 200, 200)
                )
                displaytext(
                    l[0:10], [20, 90 + co * FONT_SIZE], 255, color=(255, 255, 255)
                )
                displaytext(
                    f"{size}b", [120, 90 + co * FONT_SIZE], 255, color=(200, 200, 200)
                )
                if date != 0:
                    displaytext(
                        f"{datetime.date.fromtimestamp(date)}",
                        [220, 90 + co * FONT_SIZE],
                        255,
                        color=(200, 200, 200),
                    )
                    displaytext(
                        f"{datetime.date.fromtimestamp(date2)}",
                        [380, 90 + co * FONT_SIZE],
                        255,
                        color=(200, 200, 200),
                    )
                else:
                    displaytext(
                        f"No main file",
                        [220, 90 + co * FONT_SIZE],
                        255,
                        color=(200, 200, 200),
                    )
                    displaytext(
                        f"No main file",
                        [380, 90 + co * FONT_SIZE],
                        255,
                        color=(200, 200, 200),
                    )
                co += 0.8

        commands.displayField(2, (40, 255, 255))
        pygame.display.flip()

    load_level(basename, silent=False)


# check_things()
commands.addField(pygame.Rect(10, 550 - FONT_SIZE * 3, 400, 32), 1)


# #print(platformo)
def DebugCircle(pos, r):
    if creatorMode:
        pygame.draw.circle(
            screen,
            (0, 255, 255),
            [pos[0] + cameraposition[0], pos[1] + cameraposition[1]],
            r,
        )


def DebuggerConsole():
    # #print('Dwarf Engine, made by @ipebyx & @prostopelmenhto')
    while True:
        f = input("in  >>> ")
        k = None
        try:
            try:
                k = eval(f)
            except:
                k = exec(f)
        except Exception as e:
            pass
            # #print('err <<<', e)
        # #print("out <<<",k)


# Thread(target=DebuggerConsole).start()


def draw_rect_alpha(surface, color, rect):  # some code stolen from sof
    shape_surf = pygame.Surface(pygame.Rect(rect).size, pygame.SRCALPHA)
    pygame.draw.rect(shape_surf, color, shape_surf.get_rect())
    surface.blit(shape_surf, rect)


def floorcheck():
    a = False
    for k in platformo:
        for m in range(debilcoords[0], debilcoords[0] + debilsize[0] + 1):
            if k.collidepoint(m, debilcoords[1] + debilsize[1]):  # проверка пола
                debilspid[1] = 0
                debilcoords[1] = k.topleft[1] - debilsize[1]
                a = True
                DebugCircle((m, debilcoords[1] + debilsize[1]), 5)
        for m in range(debilcoords[0], debilcoords[0] + debilsize[0] + 1):
            if k.collidepoint(m, debilcoords[1] + debilsize[1] - 15):  # проверка пола
                debilspid[1] = 0
                debilcoords[1] = k.topleft[1] - debilsize[1]
                a = True
                DebugCircle((m, debilcoords[1] + debilsize[1] - 15), 5)
    return a


def roofcheck():
    for k in platformo:
        if (
            k.collidepoint(debilcoords[0] + debilsize[0] / 2, debilcoords[1] -10)
            or k.collidepoint(debilcoords[0]-1, debilcoords[1] -10)
            or k.collidepoint(debilcoords[0] + debilsize[0] +1, debilcoords[1] -10)
        ):  # проверка крыши
            debilspid[1] = 0
            debilcoords[1] = k.bottom+10


def physicscheck():

    for k in platformo:
        if (
            k.collidepoint(
                debilcoords[0] + debilsize[0] + 9, debilcoords[1] + debilsize[1] / 2
            )
            or k.collidepoint(debilcoords[0] - 9, debilcoords[1] + debilsize[1] / 2)
            or k.collidepoint(
                debilcoords[0] + debilsize[0] + 9, debilcoords[1] + debilsize[1] - 3
            )
            or k.collidepoint(debilcoords[0] - 9, debilcoords[1] + debilsize[1] - 3)
            or k.collidepoint(debilcoords[0] + debilsize[0] + 7, debilcoords[1])
            or k.collidepoint(debilcoords[0] - 9, debilcoords[1])
        ):  # проверка стен
            debilspid[0] = 0

        # k.x=k.x+cameraposition[0]
        # k.y=k.y+cameraposition[1]
        mp = list(pygame.mouse.get_pos())
        mp[0] -= cameraposition[0]
        mp[1] -= cameraposition[1]

        if k.collidepoint(mp) and creatorMode and modes == "hitbox":
            draw_rect_alpha(
                screen,
                (255, 32, 32, 196),
                pygame.Rect(k.x + cameraposition[0], k.y + cameraposition[1], k.w, k.h),
            )
            if remove:
                platformo.remove(k)
                # #print(platformo)
                break
        elif creatorMode:
            draw_rect_alpha(
                screen,
                (255, 32, 32, 128),
                pygame.Rect(k.x + cameraposition[0], k.y + cameraposition[1], k.w, k.h),
            )

        if k.collidepoint(mp):
            debugRectInfo.append(f"x:{k.x},y:{k.y},w:{k.w},h:{k.h}")

        if len(textures) == 0:
            draw_rect_alpha(
                screen,
                (128, 128, 128),
                pygame.Rect(k.x + cameraposition[0], k.y + cameraposition[1], k.w, k.h),
            )
        # k.x=k.x-cameraposition[0]
        # k.y=k.y-cameraposition[1]


def DRAWTRIGGERSPLEASE():
    for i in levelplatformo:
        rect = i[0]
        kuda = i[1]
        if creatorMode:
            draw_rect_alpha(
                screen,
                (255, 255, 0, 127),
                pygame.Rect(
                    rect.x + cameraposition[0],
                    rect.y + cameraposition[1],
                    rect.w,
                    rect.h,
                ),
            )

        # #print([debilcoords[0]+debilsize[0]/2,debilcoords[1]+debilsize[1]/2],rect)
        if rect.collidepoint(
            [debilcoords[0] + debilsize[0] / 2, debilcoords[1] + debilsize[1] / 2]
        ):
            load_level(kuda)
        mp = list(pygame.mouse.get_pos())
        mp = [mp[0] - cameraposition[0], mp[1] - cameraposition[1]]
        if rect.collidepoint(mp) and creatorMode and modes == "leveltrigger" and remove:
            levelplatformo.remove(i)


def debugCheckWallsOnRight():
    # короче эта хрень возвращает значение можно ли двигатся в right
    ch = False
    for k in platformo:
        ch |= (
            k.collidepoint(
                [
                    debilcoords[0] + debilsize[0] + 7,
                    debilcoords[1] + debilsize[1] / 2 - 3,
                ]
            )
            or k.collidepoint(
                [debilcoords[0] + debilsize[0] + 7, debilcoords[1] + debilsize[1] - 3]
            )
            or k.collidepoint([debilcoords[0] + debilsize[0] + 7, debilcoords[1] - 3])
        )
    return not ch


def debugCheckWallsOnLeft():
    ch = False
    # короче эта хрень возвращает значение можно ли двигатся в left
    for k in platformo:
        ch |= (
            k.collidepoint([debilcoords[0] - 7, debilcoords[1] + debilsize[1] / 2 - 3])
            or k.collidepoint([debilcoords[0] - 7, debilcoords[1] + debilsize[1] - 3])
            or k.collidepoint([debilcoords[0] - 7, debilcoords[1] - 3])
        )
    return not ch


def getGlobalMouseCoords(withSnap):
    gp = list(pygame.mouse.get_pos())
    if withSnap:
        gp[0] = (gp[0] - cameraposition[0]) // SNAP * SNAP
        gp[1] = (gp[1] - cameraposition[1]) // SNAP * SNAP
    else:
        gp[0] = gp[0] - cameraposition[0]
        gp[1] = gp[1] - cameraposition[1]
    return gp


def displayTextures():
    disp = 0
    #print(textures)
    for i in zimagelayer: 
        #print(i)
        #print(zimagelayer[i])
        
        for x in zimagelayer[i]:
            ##print(images,x)
            n=textures[x]
            screen.blit(
                n["image"], [n["position"][0] + cameraposition[0], n["position"][1] + cameraposition[1]]
            )
            #print(x)
            """
                displaytext(
                    f'IMAGE SRC: {n["name"]}',
                    [(n["position"][0] - campos[0]), (n["position"][1] - campos[1]-FONT_SIZE)],
                    color=(127, 127, 127),
                )
                displaytext(
                    f'Z LAYER: {i}',
                    [(n["position"][0] - campos[0]), (n["position"][1] - campos[1]-FONT_SIZE*2)],
                    color=(127, 127, 127),
                )
    for l in textures:

        img = l["image"]
        rct = l["position"]
        imgrect = img.get_rect()
        reeeeeeeeeeect = pygame.Rect(
            rct[0] + cameraposition[0], rct[1] + cameraposition[1], imgrect.w, imgrect.h
        )
        # if pygame.Rect(0,0,880,550).collidepoint(reeeeeeeeeeect.topleft) or\
        #    pygame.Rect(0,0,880,550).collidepoint(reeeeeeeeeeect.topright) or\
        #    pygame.Rect(0,0,880,550).collidepoint(reeeeeeeeeeect.bottomleft) or\
        #    pygame.Rect(0,0,880,550).collidepoint(reeeeeeeeeeect.bottomright):
        screen.blit(
            img,
            pygame.Rect(rct[0] + cameraposition[0], rct[1] + cameraposition[1], 0, 0),
        )
        disp += 1
        mp = list(pygame.mouse.get_pos())
        if reeeeeeeeeeect.collidepoint(mp):
            debugTexInfo.append(f"x:{rct[0]},y:{rct[1]},w:{imgrect.w},h:{imgrect.h}")
        elif creatorMode:
            draw_rect_alpha(screen, (127, 127, 255, 127), reeeeeeeeeeect)
        mp=list(pygame.mouse.get_pos())
        mp[0]-=cameraposition[0]
        mp[1]-=cameraposition[1]
        k=img.get_rect()
        pos=pygame.Rect(rct[0]+cameraposition[0],rct[1]+cameraposition[1],0,0)
        draw_rect_alpha(screen,(0,0,255,128),k)
        
        if k.collidepoint(mp) and creatorMode:
            
            pygame.draw.rect(screen,(196,196,196),pygame.Rect(pos.x,pos.y,k.w,k.h))
            ##print(f'hovering on {id(img)}, {img}')
            if remove:
                textures.remove(l)"""
    return disp


# textures.append({"image":image,"transparency":transparency,"position":position})
holdingLeft = False
holdingRight = False
holdingKeyLeft = False
holdingKeyRight = False

ImageInit()
#print(textures)
# #print('wefwefwefw')

# #print(decals)


LM = check_things

SNAP = 15


def savelevel():
    global mc
    level = f"{str(platformo).replace('<','').replace('>','').replace('rect','pygame.Rect')}"
    total = f"'title':'{title}','fillercolor':{fillercolor},'level':{level},'images':{decals},'startpos':{debilcoords},'sco':{cameraposition},'dwarfversion':'{strv}','mapswitchtriggers':{str(levelplatformo).replace('<','').replace('>','').replace('rect','pygame.Rect')},'author':'{author}','desc':'{description}'"
    f = open(fi, mode="w")
    f.write("{" + total + "}")
    f.close()
    ####print(fi)
    mc = []


import sys

try:
    lmap = sys.argv[1]
except:
    print('\n---\ndwarf v1.4_f_1.0_dle\n'\
          'usage:\n\n'\
          f'  {__file__} [map]\n'\
          '\n'\
          '[map] - .dwf map for the engine to run\n')
    exit(0)
fi = lmap


load_level(lmap)
#print(script)
#print(linking)
ImageInit()
# #print(decals)

# del commands.fields[2]

if script:
    ab = script[0]
    #print(script)
    checking = open(ab.strip())
    chkr = checking.read()

    #print(chkr)
    platf = platformo
    playerpos = debilcoords
    playervel = debilspid

    exec(chkr)

    init()

    checking.close()







0.










while (
    running
):  ############################################################################################################

    try: #BIG MOTHERFUCKING TRY LOOP!!!!!!!!!!
        try:
            screen.fill(fillercolor)
        except:
            screen.fill(eval(fillercolor))

        DebugCircle(
            [debilcoords[0] + debilsize[0] + 5, debilcoords[1] + debilsize[1] / 2 - 3], 5
        )  # справа коллизия стен (я свм нифига не понимаю)
        DebugCircle(
            [debilcoords[0] + debilsize[0] + 5, debilcoords[1] + debilsize[1] - 3], 5
        )  # справа
        DebugCircle([debilcoords[0] + debilsize[0] + 5, debilcoords[1] - 3], 5)  # справа
        DebugCircle([debilcoords[0] - 5, debilcoords[1] + debilsize[1] / 2 - 3], 5)  # слево
        DebugCircle([debilcoords[0] - 5, debilcoords[1] + debilsize[1] - 3], 5)  # слево
        DebugCircle([debilcoords[0] - 5, debilcoords[1] - 3], 5)  # слево
        DebugCircle([debilcoords[0] + debilsize[0] / 2, debilcoords[1] - 5], 5)
        DebugCircle([debilcoords[0], debilcoords[1] - 5], 5)
        DebugCircle([debilcoords[0] + debilsize[0], debilcoords[1] - 5], 5)
        k = displayTextures()
        # #print(f'displayed {k} textures')
        floorcheck()
        physicscheck()
        DRAWTRIGGERSPLEASE()
        for n in text:
            displaytext(
                n[-1],
                [(n[0] + cameraposition[0]), (n[1] + cameraposition[1])],
                color=(n[2], n[3], n[4]),
            )
        remove = False
        for event in pygame.event.get():
            pygame.display.set_caption(title)
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_PAGEUP: raise Exception('You raised a test exception. Boo hoo!')
                if event.key == pygame.K_LEFT:
                    holdingLeft = True
                    holdingKeyLeft = True
                if event.key == pygame.K_RIGHT:
                    holdingRight = True
                    holdingKeyRight = True
                if event.key == pygame.K_UP and debilspid[1] == 0:
                    debilcoords[1] = debilcoords[1] - 1
                    debilspid[1] = -20
                if event.key == pygame.K_F1:
                    creatorMode ^= 1
                if event.key == pygame.K_F2:
                    removeDecals ^= 1
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    holdingLeft = False
                    holdingKeyLeft = False
                if event.key == pygame.K_RIGHT:
                    holdingRight = False
                    holdingKeyRight = False
                if event.key == pygame.K_RIGHT:
                    holdingRight = False
                    holdingKeyRight = False
            # F
        

        cameraposition = [
            -debilcoords[0] + 320 - debilsize[0],
            -debilcoords[1] + 240 - debilsize[1],
        ]
        camsomewhere.append(cameraposition)

        smoothness=72

        if len(camsomewhere) > smoothness:
            del camsomewhere[0]
        sumcamx = 0
        sumcamy = 0
        for m in camsomewhere:
            sumcamx += m[0]
        for m in camsomewhere:
            sumcamy += m[1]
        cameraposition = [(sumcamx / smoothness),(sumcamy / smoothness)]


        
        if debugCheckWallsOnLeft() and holdingKeyLeft:
            debilspid[0] = -7
        elif debugCheckWallsOnRight() and holdingKeyRight:
            debilspid[0] = 7
        else:
            debilspid[0] = 0

        if creatorMode:
            for n in triggers:
                draw_rect_alpha(
                    screen,
                    (255, 255, 0, 64),
                    [(n[0] + cameraposition[0]), (n[1] + cameraposition[1]), n[2], n[3]],
                )
                displaytext(
                    f"TRIGGER BOX",
                    [(n[0] + cameraposition[0]), (n[1] + cameraposition[1])],
                    color=(0, 0, 0),
                )
                displaytext(
                    f"ID={n[-1]}",
                    [(n[0] + cameraposition[0]), (n[1] + FONT_SIZE + cameraposition[1])],
                    color=(0, 0, 0),
                )
            if len(mc) == 2:
                if modes == "leveltrigger":
                    scanx = mc[0][0]
                    scany = mc[0][1]
                    scanw = abs(mc[1][0] - mc[0][0])
                    scanh = abs(mc[1][1] - mc[0][1])
                    h = input("rederict to map? ")
                    levelplatformo.append([pygame.Rect([scanx, scany], [scanw, scanh]), h])
                    ###print('trigger plac')
                    for j in levelplatformo:
                        if j.w == 0 and j.h == 0 or j.w == 0 or j.h == 0:
                            ###print("null hitbox, deleting")
                            platformo.remove(j)
                    savelevel()
                elif modes == "hitbox":
                    scanx = mc[0][0]
                    scany = mc[0][1]
                    scanw = abs(mc[1][0] - mc[0][0])
                    scanh = abs(mc[1][1] - mc[0][1])
                    platformo.append(pygame.Rect([scanx, scany], [scanw, scanh]))
                    ###print('platform plac')
                    for j in platformo:
                        if j.w == 0 and j.h == 0 or j.w == 0 or j.h == 0:
                            ###print("null hitbox, deleting")
                            platformo.remove(j)
                    savelevel()
            if len(mc) == 1:
                scanx = mc[0][0]
                scany = mc[0][1]
                k = pygame.mouse.get_pos()
                scanw = abs(k[0] - mc[0][0] - cameraposition[0])
                scanh = abs(k[1] - mc[0][1] - cameraposition[1])
                pygame.draw.rect(
                    screen,
                    (64, 64, 64),
                    pygame.Rect(
                        (scanx // SNAP * SNAP + cameraposition[0]),
                        (scany // SNAP * SNAP + cameraposition[1]),
                        scanw // SNAP * SNAP,
                        scanh // SNAP * SNAP,
                    ),
                )
        roofcheck()
        debilcoords[0] += debilspid[0]
        debilcoords[1] += debilspid[1]
        if not floorcheck():
            debilspid[1] += g / 5
        for k in linking:
            if k[0].collidepoint(debilcoords):
                load_level(k[1])
        a = clock.get_fps()
        if creatorMode:
            displaytext(f"Affecting filter: {modes}", [400, 0])

            displaytext(f"camera pos   : {list(map(round,cameraposition))}", [0, 0])
            displaytext(f"snap         : {SNAP}", [0, FONT_SIZE])
            displaytext(f"FPS          : {round(a,3)}", [0, FONT_SIZE * 2])
            displaytext(f"target FPS   : {round(FPS,3)}", [0, FONT_SIZE * 3])
            # displaytext(f'del dec/hitb : {"deleting decals|textures"*removeDecals+"deleting hitboxes"*(1-removeDecals)}',[0,FONT_SIZE*4])
            displaytext(
                f"player pos   : {list(map(round,debilcoords))}", [0, FONT_SIZE * 4]
            )
            displaytext(f"decals num   : {len(decals)}", [0, FONT_SIZE * 5])
            displaytext(f"textures num : {len(textures)}", [0, FONT_SIZE * 6])
            displaytext(f"disp.tex.num : {k}", [0, FONT_SIZE * 7])
            displaytext(f"tex==dec?    : {len(decals)==len(textures)}", [0, FONT_SIZE * 8])
            displaytext(f"debugRectInfo: {debugRectInfo}", [0, FONT_SIZE * 9])
            displaytext(f"debugTexInfo : {debugTexInfo}", [0, FONT_SIZE * 10])
            displaytext(
                f"global m.pos : {list(map(round,getGlobalMouseCoords(False)))}",
                [0, FONT_SIZE * 11],
            )
            displaytext(f"map version  : {strv}", [0, FONT_SIZE * 12])
            displaytext(f'map name     : "{fi}"', [0, FONT_SIZE * 13])

            displaytext(f"--------------", [0, FONT_SIZE * 14])
            displaytext(f"debug mode. to turn it off, press f12", [0, FONT_SIZE * 15])

            displaytext(f'author: "{author}"', [0, 550 - FONT_SIZE])
            displaytext(f'description: "{description}"', [400, 550 - FONT_SIZE])

            commands.displayField(1, (200, 200, 200))

            debugRectInfo = []
            debugTexInfo = []

        gp = list(pygame.mouse.get_pos())
        POS = [
            (gp[0] - cameraposition[0]) // SNAP * SNAP,
            (gp[1] - cameraposition[1]) // SNAP * SNAP,
        ]
        POS[0] += cameraposition[0]
        POS[1] += cameraposition[1]

        if creatorMode:
            screen.blit(cursor, POS)
        ksc = screen.convert_alpha()
        ksc.set_alpha(5)

        ksc.blit(screen, pygame.Rect(0, 0, ksc.get_rect().w, ksc.get_rect().h))

        if script:
            tick()
            for trig in triggers:
                if pygame.Rect(trig[0:4]).collidepoint(debilcoords):
                    trigger(trig[-1])

        pygame.draw.rect(
            screen,
            (255, 255, 255),
            pygame.Rect(
                [debilcoords[0] + cameraposition[0], debilcoords[1] + cameraposition[1]],
                debilsize,
            ),
        )

        pygame.display.flip()

        g = 9.81
        clock.tick(FPS)
    except Exception as e:
        k = traceback.format_exception()
        CEMB(f'Engine error!\n'\
              '-----\n'\
             f'{k}'\
             f'-----\n{e}'\
                )
        exit()
