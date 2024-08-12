
x=225
marked=[]
def init():
    global marked
    print('Script init')
    for n in platf:
        if n==pygame.Rect(x,135,60,30):
            marked.append(platf.index(n))
        if n==pygame.Rect(30,270,30,90):
            marked.append(platf.index(n))
        
def tick():
    nl=[]
def trigger(id):
    if id==0 and (playerpos[1])<=340:

        for trig in triggers:
            print(trig,playerpos[1])
            if trig[-1]==id:
                trig[1]=trig[1]+1
                print('adding')
                platf[marked[0]].y=platf[marked[0]].y+1
                break
    elif id==0 and (playerpos[1])>340:
        for trig in triggers:
            if trig[-1]==id:
                triggers.remove(trig)
    elif id==1:
        platf[marked[1]].y=max(platf[marked[1]].y-3,225)
    else:
        platf[marked[1]].y=max(platf[marked[1]].y+3,225)

        print('beep')