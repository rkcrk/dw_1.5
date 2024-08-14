from math import *
from tkinter import Tk
from tkinter.filedialog import askopenfilename
import tkinter.filedialog as tf
import easygui as eg
import ctypes
import sys
from difflib import SequenceMatcher
import os



def cutcapital(s):
    if s[0] == s[0].capitalize():
        return s[1:]
    else:
        return s


SNAP = 15
DIV = 1
hitboxes = []
images = []
decals = []
zimagelayer={}
linking = []
text = []
campos = [0, 0]

print(os.path.dirname(os.path.abspath(__file__)))

import pygame

screen = pygame.display.set_mode((800, 550), pygame.ASYNCBLIT)


def loadify(imgname):
    return pygame.image.load(imgname).convert_alpha()


Tk().withdraw()


def Mbox(title, text, style):
    return ctypes.windll.user32.MessageBoxW(0, text, title, style)


def CEMB(text):
    return ctypes.windll.user32.MessageBoxW(0, text, "An exception occured", 16)


def ImageInit(silent=True):
    global decals
    global images
    images = []
    for dec in decals:
        try:
            image = loadify(dec[2])
        except:
            if not silent:
                CEMB(
                    f'ТЕКСТУРА "{dec[2]}" НЕ НАЙДЕНА /\nTEXTURE "{dec[2]}" IS NOT FOUND'
                )
                raise FileNotFoundError(f"texture not found (context: {dec[2]})")
            print(f'ТЕКСТУРА "{dec[2]}" НЕ НАЙДЕНА')

            image = loadify("engine/decals/dwarf_missing.png")
        transparency = int(dec[3])
        image.set_alpha(transparency)
        position = [dec[0], dec[1]]
        images.append(
            {
                "image": image,
                "transparency": transparency,
                "position": position,
                "name": dec[-2],
            }
        )


def parselevel(file):

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
    global camsp
    global author
    global title
    global desc
    global color
    global ver
    global linking
    global decals
    global script
    global text
    global triggers
    global zimagelayer
    global r
    global b
    global g
    zimagelayer={}
    SNAP = 15
    DIV = 1
    script = []
    text = []
    triggers = []
    decalcounter=0
    hitboxes = []
    images = []
    decals = []
    linking = []
    campos = [0, 0]
    for line in m:
        sl = line.split(" ", 1)
        sh = sl[1]
        if sl[0] == ".IP":
            x, y = list(map(int, sh.split(",")))
            plrspwn = [x, y]
            print(f"player spawn at {x=},{y=}")
        if sl[0] == ".ICP":
            x, y = list(map(int, sh.split(",")))
            camsp = [x, y]
            print(f"camera spawn at {x=},{y=}")
        if sl[0] == ".A":
            st = sh.split(",")[-1].strip()
            author = st
            print(f"author: {st}")
        if sl[0] == ".T":
            st = sh.split(",")[-1].strip()
            title = st
            print(f"title: {st}")
        if sl[0] == ".D":
            st = sh.split(",")[-1].strip()
            desc = st
            print(f"description: {st}")
        if sl[0] == ".F":
            r, g, b = list(map(int, sh.split(",")))
            color = (r, g, b)
            print(f"filler color: {r=},{g=},{b=}")
        if sl[0] == ".DV":
            st = sh.split(",")[-1].strip()
            print(f"version: {st}")
            ver = st
        if sl[0] == "H":

            x, y, w, h = list(map(int, sh.split(",")))
            print(f"hitbox at {x=},{y=} with {w=},{h=}")
            hitboxes.append([x, y, w, h])
        if sl[0] == "L":

            x, y, w, h = list(map(int, sh.split(",")[0:4]))
            l = sh.split(",")[4].strip()
            print(f"linking hitbox at {x=},{y=} with {w=},{h=} linking to {l=}")
            linking.append([x, y, w, h, l])
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
                    zimagelayer[z].append(decalcounter)
                except:
                    zimagelayer[z]=[decalcounter]
                print(f'found image w/ z layer technology, {z=}')
            except Exception as r:
                print(f'{r}\n---\nplease keep in mind that THIS decal will show behind every decal with Z layer eg. z layer =-99')
                try:
                    zimagelayer[-99].append(decalcounter)
                except:
                    zimagelayer[-99]=[decalcounter]
                
            print(f"image at {x=},{y=} linking to {l} w/ transparency {t}")
            decals.append([x, y, l, t])
            decalcounter+=1
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

            print(list(map(int, sh.split(",")[:-1])))
            print(int(sh.split(",")[-1]))
            id = int(sh.split(",")[-1])
            x, y, w, h = list(map(int, sh.split(",")[:-1]))
            triggers.append([x, y, w, h, id])
            print(f"trigger at {x=},{y=} with {w=},{h=} w/ {id=}")
        if sl[0] == "S":

            script.append(sh.strip())
            print(f"script w/ name {sh.strip()}")
    zimagelayer= dict(sorted(zimagelayer.items()))
    ImageInit()


filename = askopenfilename()
if filename == "":
    CEMB(
        "Looks like you've closed the askopenfilename box before selecting anything. Program will NOT proceed its job further."
    )
    sys.exit(0)
else:
    parselevel(filename)

FONT_SIZE = 20
pygame.font.init()
font = pygame.font.SysFont("@MS Gothic", FONT_SIZE)
clk = pygame.time.Clock()
menu = loadify("engine/decals/menu.png")
scriptimg = loadify("engine/decals/Dwarf_Script.png")
reloadimg = loadify("engine/decals/Dwarf_Reloading.png")

cursor = loadify("engine/decals/Dwarf_Cursor.png")


def displaytext(text, pos, transparency=210, color=(0, 0, 1)):
    if color == (0, 0, 1):
        color = (255 - color[0], 255 - color[1], 255 - color[2])
    text = font.render(text, False, color).convert_alpha()
    text.set_alpha(transparency)
    screen.blit(text, pos)


def draw_rect_alpha(surface, color, rect):
    shape_surf = pygame.Surface(pygame.Rect(rect).size, pygame.SRCALPHA)
    pygame.draw.rect(shape_surf, color, shape_surf.get_rect())
    surface.blit(shape_surf, rect)


def save(manual=False, name="temp.dwf"):
    global filename
    print("save/export")
    h = "" 
    imgidx=0
    for i in hitboxes:
        h += f"H {i[0]},{i[1]},{i[2]},{i[3]}\n"
    for i in zimagelayer: 
        for x in zimagelayer[i]:
            n=images[x]
            h += (
                f"I {n['position'][0]},{n['position'][1]},{n['name']},{n['transparency']},{i}\n"
            )
    """for i in images:
        
        
        h += (
            f"I {i['position'][0]},{i['position'][1]},{i['name']},{i['transparency']},{}\n"
        )
        imgidx+=1"""
    for i in linking:
        h += f"L {i[0]},{i[1]},{i[2]},{i[3]},{i[4]}\n"
    for i in text:
        h += f"T {i[0]},{i[1]},{i[2]},{i[3]},{i[4]},{i[5]}\n"
    for i in triggers:
        h += f"R {i[0]},{i[1]},{i[2]},{i[3]},{i[4]}\n"
    for i in script:
        h += f"S {i}\n"

    h += f".IP {plrspwn[0]},{plrspwn[1]}\n"
    h += f".ICP {plrspwn[0]},{plrspwn[1]}\n"
    h += f".A AUTHOR\n"
    h += f".T DLE _Standalone Map\n"
    h += f".D A map made in the Dwarf Level Editor _Standalone program\n"
    h += f".F {r},{g},{b}\n"
    h += f".DV 1.4\n"

    if not manual:
        f = tf.asksaveasfile(filetypes=(("Dwarf 1.4 level file", "*.dwf"),))
        f.write(h)
        f.close()
        filename = f.name
    else:
        f = open(name, mode="w")
        f.write(h)
        f.close()
        filename = name


LEFT = False
RIGHT = False
UP = False
DOWN = False
CTRL = False
rel = False

leftborderjob = 340
rightclickjob = False
running = True

mode = "hitbox"
mc = []
time = 0
tickswithoutskewing = 0
skew = 0

displaymode=0


rightclickjobpos = [-7000, 0]
ImageInit()


print(zimagelayer)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0]:
            if (
                pygame.Rect(800 - 64, 550 / 2, 64, 550 / 2).collidepoint(
                    pygame.mouse.get_pos()
                )
                and script
            ):
                Mbox(f"Info about level", f"Script path: {script[0]}", 0)
        if event.type == pygame.MOUSEBUTTONDOWN:
            gp = list(pygame.mouse.get_pos())
            tp = [
                (campos[0] + gp[0]) // SNAP * SNAP,
                (campos[1] + gp[1]) // SNAP * SNAP,
            ]
            print(f"click at global {tp}")
        if event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0]:
            gp = list(pygame.mouse.get_pos())
            mc.append(
                [(campos[0] + gp[0]) // SNAP * SNAP, (campos[1] + gp[1]) // SNAP * SNAP]
            )
        if (
            event.type == pygame.MOUSEBUTTONDOWN
            and pygame.mouse.get_pressed()[0]
            and mode == "d"
        ):
            mc = []
            gp = list(pygame.mouse.get_pos())
            tp = [(gp[0] + campos[0]), (gp[1] + campos[1])]
            for n in hitboxes:
                if pygame.Rect(n).collidepoint(tp):
                    hitboxes.remove(n)
                    print("goodbye hb")
                    break

            for n in linking:
                if pygame.Rect(n[0:4]).collidepoint(tp):
                    linking.remove(n)
                    print("goodbye lb")
                    break
            for nj in images:
                rct = nj["image"].get_rect()
                reeeeeeeeeeect = pygame.Rect(
                    (rct[0] + nj["position"][0]),
                    (rct[1] + nj["position"][1]),
                    rct.w,
                    rct.h,
                )

                if reeeeeeeeeeect.collidepoint(tp):
                    images.remove(nj)
                    print("goodbye img")
                    decals.remove(
                        [
                            reeeeeeeeeeect.x,
                            reeeeeeeeeeect.y,
                            nj["name"],
                            nj["transparency"],
                        ]
                    )
                    break
            for n in triggers:
                if pygame.Rect(n[0:4]).collidepoint(tp):
                    linking.remove(n)
                    print("goodbye tb")
                    break
        if event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[2]:
            cp = pygame.mouse.get_pos()
            rightclickjob ^= 1
            rightclickjobpos = [
                ((cp[0] + campos[0]) // SNAP * SNAP - campos[0]),
                ((cp[1] + campos[1]) // SNAP * SNAP - campos[1]),
            ]
        if event.type == pygame.MOUSEBUTTONDOWN:
            if pygame.Rect(0, -40 + skew, 40, 40).collidepoint(pygame.mouse.get_pos()):
                print("hitbox")
                mode = "hb"
                mc = []
            if pygame.Rect(40, -40 + skew, 40, 40).collidepoint(pygame.mouse.get_pos()):
                print("link")
                mode = "lb"
                mc = []
            if pygame.Rect(80, -40 + skew, 40, 40).collidepoint(pygame.mouse.get_pos()):
                print("trigger")
                mode = "tb"
                mc = []
            if pygame.Rect(120, -40 + skew, 40, 40).collidepoint(
                pygame.mouse.get_pos()
            ):
                print("text")
                mode = "tx"
                mc = []
            if pygame.Rect(160, -40 + skew, 40, 40).collidepoint(
                pygame.mouse.get_pos()
            ):
                print("delete")
                mode = "d"
                mc = []
            if pygame.Rect(200, -40 + skew, 40, 40).collidepoint(
                pygame.mouse.get_pos()
            ):
                save()
                mc = []
            if pygame.Rect(240, -40 + skew, 40, 40).collidepoint(
                pygame.mouse.get_pos()
            ):
                print("open")
                filename = askopenfilename(title="Select the file you want to open")
                if filename == "":
                    CEMB(
                        "Looks like you've closed the askopenfilename box before selecting anything. Program will NOT proceed its loading job further."
                    )
                else:
                    parselevel(filename)
            if pygame.Rect(280, -40 + skew, 40, 40).collidepoint(
                pygame.mouse.get_pos()
            ):
                save(True, "maps/temp.dwf")
                os.system(f'start /b /wait python game_engine.py "maps/temp.dwf"')

            if (
                pygame.Rect(
                    [rightclickjobpos[0] + 14, rightclickjobpos[1] + 14], [200, 30]
                ).collidepoint(pygame.mouse.get_pos())
                and rightclickjob
            ):
                print("DELEEE")
                tp = [
                    (rightclickjobpos[0] + campos[0]),
                    (rightclickjobpos[1] + campos[1]),
                ]
                for n in hitboxes:
                    if pygame.Rect(n).collidepoint(tp):
                        hitboxes.remove(n)
                        print("goodbye hb")
                        break

                for n in linking:
                    if pygame.Rect(n[0:4]).collidepoint(tp):
                        linking.remove(n)
                        print("goodbye lb")
                        break
                for n in triggers:
                    if pygame.Rect(n[0:4]).collidepoint(tp):
                        triggers.remove(n)
                        print("goodbye tb")
                        break

                for nj in images:
                    rct = nj["image"].get_rect()
                    reeeeeeeeeeect = pygame.Rect(
                        (rct[0] + nj["position"][0]),
                        (rct[1] + nj["position"][1]),
                        rct.w,
                        rct.h,
                    )
                    print(reeeeeeeeeeect)

                    if reeeeeeeeeeect.collidepoint(tp):
                        i=Mbox('Select the image you want to delete',f'Info about image:\n{reeeeeeeeeeect.__repr__()}\n{nj["name"]=}',48 +1)
                        print(i)
                        if i==1:
                            images.remove(nj)
                            print("goodbye img")
                            decals.remove(
                                [
                                    reeeeeeeeeeect.x,
                                    reeeeeeeeeeect.y,
                                    nj["name"],
                                    nj["transparency"],
                                ]
                            )

                        #else:break
                mc = []
                # rightclickjob=False
            if (
                pygame.Rect(
                    [rightclickjobpos[0] + 14, rightclickjobpos[1] + 14 + 30], [200, 30]
                ).collidepoint(pygame.mouse.get_pos())
                and rightclickjob
            ):
                mc = []

                mode = "hb"

                mc.append(
                    [
                        (campos[0] + rightclickjobpos[0]) // SNAP * SNAP,
                        (campos[1] + rightclickjobpos[1]) // SNAP * SNAP,
                    ]
                )
                rightclickjob = False
            if (
                pygame.Rect(
                    [rightclickjobpos[0] + 14, rightclickjobpos[1] + 14 + 30 * 2],
                    [200, 30],
                ).collidepoint(pygame.mouse.get_pos())
                and rightclickjob
            ):
                print("create linkbox")
                mc = []

                mode = "lb"
                mc.append(
                    [
                        (campos[0] + rightclickjobpos[0]) // SNAP * SNAP,
                        (campos[1] + rightclickjobpos[1]) // SNAP * SNAP,
                    ]
                )
                rightclickjob = False
            if (
                pygame.Rect(
                    [rightclickjobpos[0] + 14, rightclickjobpos[1] + 14 + 30 * 3],
                    [200, 30],
                ).collidepoint(pygame.mouse.get_pos())
                and rightclickjob
            ):
                print("create image")
                mode = "i"
                f = askopenfilename(
                    title="Select an image (you cannot select the image outside the engine)"
                )
                string1 = __file__
                string2 = f.replace("/", "\\")
                match = SequenceMatcher(None, string1, string2).find_longest_match()
                n = string1[match.a : match.a + match.size]

                try:
                    s2 = string2.replace(string1[match.a : match.a + match.size], "")[
                        1:
                    ]
                    decals.append(
                        [
                            (campos[0] + rightclickjobpos[0]) // SNAP * SNAP,
                            (campos[1] + rightclickjobpos[1]) // SNAP * SNAP,
                            s2,
                            255,
                        ]
                    )
                    ImageInit(True)
                except:
                    decals.remove(
                        [
                            (campos[0] + rightclickjobpos[0]) // SNAP * SNAP,
                            (campos[1] + rightclickjobpos[1]) // SNAP * SNAP,
                            s2,
                            255,
                        ]
                    )
                    s2 = string2.replace(string1[match.a : match.a + match.size], "")
                    decals.append(
                        [
                            (campos[0] + rightclickjobpos[0]) // SNAP * SNAP,
                            (campos[1] + rightclickjobpos[1]) // SNAP * SNAP,
                            s2,
                            255,
                        ]
                    )
                    try:
                        ImageInit(False)
                    except:
                        print("there is nothing we can do")
                mc = []
                rightclickjob = False
            if (
                pygame.Rect(
                    [rightclickjobpos[0] + 14, rightclickjobpos[1] + 14 + 30 * 4],
                    [200, 30],
                ).collidepoint(pygame.mouse.get_pos())
                and rightclickjob
            ):

                plrspwn = [
                    (rightclickjobpos[0] + campos[0]),
                    (rightclickjobpos[1] + campos[1]),
                ]
                mc = []
                rightclickjob = False
            if (
                pygame.Rect(
                    [rightclickjobpos[0] + 14, rightclickjobpos[1] + 14 + 30 * 5],
                    [200, 30],
                ).collidepoint(pygame.mouse.get_pos())
                and rightclickjob
            ):
                save()
            if (
                pygame.Rect(
                    [rightclickjobpos[0] + 14, rightclickjobpos[1] + 14 + 30 * 6],
                    [200, 30],
                ).collidepoint(pygame.mouse.get_pos())
                and rightclickjob
            ):
                print("new project ")
                mode = "d"
                mc = []
                SNAP = 15
                DIV = 1
                hitboxes = []
                images = []
                decals = []
                linking = []
                campos = [0, 0]
                running = True
                LEFT = False
                RIGHT = False
                UP = False
                DOWN = False
                rightclickjob = False
                mode = "hitbox"
                mc = []
                time = 0
                skew = 0
        if (
            event.type == pygame.MOUSEBUTTONDOWN
            and not pygame.mouse.get_pressed()[2]
            and rightclickjob
        ):
            rightclickjob = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                LEFT = True
            if event.key == pygame.K_RIGHT:
                RIGHT = True
            if event.key == pygame.K_UP:
                UP = True
            if event.key == pygame.K_DOWN:
                DOWN = True
            if event.key == pygame.K_LCTRL:
                CTRL = True
            if event.key == pygame.K_q:
                SNAP -= 5 * (SNAP > 6)
            if event.key == pygame.K_e:
                SNAP += 5
            if event.key == pygame.K_r:
                ImageInit()
                rel = True

            if event.key==pygame.K_1:displaymode^=0b00001
            if event.key==pygame.K_2:displaymode^=0b00010
            if event.key==pygame.K_3:displaymode^=0b00100
            if event.key==pygame.K_4:displaymode^=0b01000
            if event.key==pygame.K_5:displaymode^=0b10000
            if event.key==pygame.K_0:displaymode^=0b100000
            
            
            
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                LEFT = False
            if event.key == pygame.K_RIGHT:
                RIGHT = False
            if event.key == pygame.K_UP:
                UP = False
            if event.key == pygame.K_DOWN:
                DOWN = False
            if event.key == pygame.K_LCTRL:
                CTRL = False
        if event.type == pygame.MOUSEWHEEL:
            if not CTRL:
                campos[1] -= event.y * 24
            if CTRL:
                campos[0] -= event.y * 24

    campos[0] = campos[0] - 6 * LEFT + 6 * RIGHT
    campos[1] = campos[1] - 6 * UP + 6 * DOWN

    screen.fill(color)

    if pygame.Rect(800 - 64, 550 / 2, 64, 550 / 2).collidepoint(pygame.mouse.get_pos()):
        leftborderjob = max(leftborderjob - 12, 32)
    else:
        leftborderjob = min(leftborderjob + 15, 340 - 32)



    if displaymode&0b00001==0:
        for i in zimagelayer: 
            for x in zimagelayer[i]:
                try:
                    n=images[x]
                except:
                    del x
                screen.blit(
                    n["image"], [n["position"][0] - campos[0], n["position"][1] - campos[1]]
                )
                if displaymode&0b100000:
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
                    
    if displaymode&0b00010==0:
        for n in hitboxes:
            draw_rect_alpha(
                screen,
                (128, 128, 128, 64),
                [(n[0] - campos[0]), (n[1] - campos[1]), n[2], n[3]],
            )
    if displaymode&0b00100==0:
        for n in linking:
            draw_rect_alpha(
                screen,
                (100, 100, 64, 64),
                [(n[0] - campos[0]), (n[1] - campos[1]), n[2], n[3]],
            )
            displaytext(
                f"TELEPORTS TO {n[-1]}",
                [(n[0] - campos[0]), (n[1] - campos[1])],
                color=(0, 0, 0),
            )
    if displaymode&0b01000==0:
        for n in text:
            displaytext(
                n[-1], [(n[0] - campos[0]), (n[1] - campos[1])], color=(n[2], n[3], n[4])
            )
    if displaymode&0b10000==0:
        for n in triggers:
            draw_rect_alpha(
                screen,
                (255, 255, 0, 64),
                [(n[0] - campos[0]), (n[1] - campos[1]), n[2], n[3]],
            )
            displaytext(
                f"TRIGGER BOX", [(n[0] - campos[0]), (n[1] - campos[1])], color=(0, 0, 0)
            )
            displaytext(
                f"ID={n[-1]}",
                [(n[0] - campos[0]), (n[1] + FONT_SIZE - campos[1])],
                color=(0, 0, 0),
            )

    displaytext(f"Flags: {'i'*(displaymode&0b00001==0)}{'h'*(displaymode&0b00010==0)}{'l'*(displaymode&0b00100==0)}{'x'*(displaymode&0b01000==0)}{'t'*(displaymode&0b10000==0)}{'s'*(displaymode&0b100000==0)}",[0, 550 - FONT_SIZE*2])


    n = pygame.Surface(screen.get_size(), pygame.SRCALPHA).convert_alpha()
    n.set_alpha(64)

    if len(mc) == 2:
        scanx = mc[0][0]
        scany = mc[0][1]
        scanw = abs(mc[1][0] - mc[0][0])
        scanh = abs(mc[1][1] - mc[0][1])

        kn = [scanx, scany, scanw, scanh]
        if mode == "hb":
            hitboxes.append(kn)
            print(kn)
        if mode == "lb":
            f = askopenfilename(title="Where does it link to?")
            string1 = __file__
            string2 = f.replace("/", "\\")
            match = SequenceMatcher(None, string1, string2).find_longest_match()
            # nqqqq=string1[match.a:match.a + match.size]

            s2 = cutcapital(
                string2.replace(string1[match.a : match.a + match.size], "")[:]
            )
            linking.append(kn + [s2])
            print(linking)
        if mode == "tb":

            triggers.append(kn + [0])
            print(kn)

        mc = []
    if len(mc) == 1:
        nc = int(pygame.math.lerp(0, 255, abs(sin(time / 15)) / 3 + 0.2))
        if mode == "tx":
            k = eg.enterbox("What text you want to appear?")
            text.append([gp[0] + campos[0], gp[1] + campos[1], 0, 0, 0, k])
            mc = []

    cp = pygame.mouse.get_pos()
    screen.blit(
        cursor,
        [
            (cp[0] + campos[0]) // SNAP * SNAP - campos[0],
            (cp[1] + campos[1]) // SNAP * SNAP - campos[1],
        ],
    )

    displaytext(
        "PLAYER SPAWN",
        [(plrspwn[0] - campos[0]), (plrspwn[1] - campos[1])],
        color=(0, 0, 0),
    )

    pygame.draw.line(
        n,
        (255, 255, 0),
        [(plrspwn[0] - campos[0]) - 5, (plrspwn[1] - campos[1]) - 5],
        [(plrspwn[0] - campos[0]) + 5, (plrspwn[1] - campos[1]) + 5],
        3,
    )
    pygame.draw.line(
        n,
        (255, 255, 0),
        [(plrspwn[0] - campos[0]) + 5, (plrspwn[1] - campos[1]) - 5],
        [(plrspwn[0] - campos[0]) - 5, (plrspwn[1] - campos[1]) + 5],
        3,
    )

    cSNAP = SNAP
    for k in range(-600, 600):

        pygame.draw.line(
            n,
            (255, 255, 255),
            [(k * cSNAP - campos[0]), (700 - campos[1])],
            [(k * cSNAP - campos[0]), (-700 - campos[1])],
        )
    for k in range(-600, 600):
        pygame.draw.line(
            n,
            (255, 255, 255),
            [(1400 - campos[0]), (k * cSNAP - campos[1])],
            [(-1400 - campos[0]), (k * cSNAP - campos[1])],
        )
    pygame.draw.line(
        n,
        (255, 0, 0),
        [(0 - campos[0]), (-8000 - campos[1])],
        [(0 - campos[0]), (8000 - campos[1])],
        3,
    )
    pygame.draw.line(
        n,
        (0, 0, 255),
        [(-8000 - campos[0]), (0 - campos[1])],
        [(8000 - campos[0]), (0 - campos[1])],
        3,
    )
    screen.blit(n, [0, 0])
    screen.blit(menu, [0, -40 + skew])
    displaytext(
        f'"{title}" by {author}',
        [0, skew + 5],
        color=(255, 255, 255),
        transparency=int(255 - skew / 40 * 128) - tickswithoutskewing,
    )
    displaytext(
        f"{desc}",
        [0, skew + 30],
        color=(255, 255, 255),
        transparency=int(255 - skew / 40 * 128 - tickswithoutskewing),
    )
    displaytext(
        f"{SNAP=}", [0, 550 - FONT_SIZE], color=(255, 255, 255), transparency=int(127)
    )

    if script:
        displaytext(
            f"This map uses a script",
            [800 - 300 + leftborderjob, 550 - FONT_SIZE - 6],
            color=(255, 255, 255),
            transparency=int(210),
        )
        screen.blit(scriptimg, [800 - 340 + leftborderjob, 550 - 32])

    if cp[1] < 80:
        skew = min(skew + 4, 40)
        tickswithoutskewing = -255
    else:
        skew = max(skew - 5, 0)
        tickswithoutskewing += 3




    



    if rightclickjob:
        x, y = rightclickjobpos
        bord = 3
        h = 30
        w = 200
        nc = int(pygame.math.lerp(0, 255, abs(sin(time / 30)) / 3 + 0.2))
        pygame.draw.circle(screen, (nc, nc, 255), [x, y], 20, 4)

        x += 14
        y += 14

        pygame.draw.rect(
            screen, (80, 80, 80), pygame.Rect(x, y, w, h * 7), border_radius=bord
        )
        pygame.draw.rect(
            screen,
            (100, 100, 100),
            pygame.Rect(x + bord, y + bord, w - bord * 2, h - bord * 2),
            border_radius=bord,
        )
        displaytext(
            "Delete",
            [x + 2 + bord, y + 2 + bord],
            transparency=255,
            color=(255, 255, 255),
        )
        pygame.draw.rect(
            screen,
            (100, 100, 100),
            pygame.Rect(x + bord, y + bord + 30, w - bord * 2, h - bord * 2),
            border_radius=bord,
        )
        displaytext(
            "Create Hitbox",
            [x + 2 + bord, y + 2 + bord + 30],
            transparency=255,
            color=(255, 255, 255),
        )
        pygame.draw.rect(
            screen,
            (100, 100, 100),
            pygame.Rect(x + bord, y + bord + 30 * 2, w - bord * 2, h - bord * 2),
            border_radius=bord,
        )
        displaytext(
            "Create Linkbox",
            [x + 2 + bord, y + 2 + bord + 30 * 2],
            transparency=255,
            color=(255, 255, 255),
        )
        pygame.draw.rect(
            screen,
            (100, 100, 100),
            pygame.Rect(x + bord, y + bord + 30 * 3, w - bord * 2, h - bord * 2),
            border_radius=bord,
        )
        displaytext(
            "Create Image",
            [x + 2 + bord, y + 2 + bord + 30 * 3],
            transparency=255,
            color=(255, 255, 255),
        )
        pygame.draw.rect(
            screen,
            (100, 100, 100),
            pygame.Rect(x + bord, y + bord + 30 * 4, w - bord * 2, h - bord * 2),
            border_radius=bord,
        )
        displaytext(
            "Set spawn here",
            [x + 2 + bord, y + 2 + bord + 30 * 4],
            transparency=255,
            color=(255, 255, 255),
        )
        pygame.draw.rect(
            screen,
            (100, 100, 100),
            pygame.Rect(x + bord, y + bord + 30 * 5, w - bord * 2, h - bord * 2),
            border_radius=bord,
        )
        displaytext(
            "Save/Export",
            [x + 2 + bord, y + 2 + bord + 30 * 5],
            transparency=255,
            color=(255, 255, 255),
        )
        pygame.draw.rect(
            screen,
            (100, 100, 100),
            pygame.Rect(x + bord, y + bord + 30 * 6, w - bord * 2, h - bord * 2),
            border_radius=bord,
        )
        displaytext(
            "New project",
            [x + 2 + bord, y + 2 + bord + 30 * 6],
            transparency=255,
            color=(255, 255, 255),
        )
    if rel:
        screen.blit(reloadimg, (40, 40))
    rel = False
    pygame.display.flip()
    clk.tick(60)
    time += 1
