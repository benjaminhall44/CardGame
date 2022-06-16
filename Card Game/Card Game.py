import random,pygame,math
pygame.init()
board = pygame.image.load("graphics/board.png")
screensize = board.get_size()
screen = pygame.display.set_mode(screensize)
class card:
    def __init__(self,name):
        self.name = name
        self.texture = pygame.image.load("graphics/%s.png" % name)
        self.magnified = pygame.image.load("graphics/%smagnified.png" % name)
        self.size = self.texture.get_size()
        self.magsize = self.magnified.get_size()
        self.flipped = False
        self.position = [100,100]
        self.height = 0
        self.rotation = 0
        self.back = ""
    def place(self):
        global cards
        h = 0
        for d in cards:
            if d != self and d.position[0] + d.size[0] > self.position[0] and d.position[0] < self.position[0] + self.size[0] and d.position[1] + d.size[1] > self.position[1] and d.position[1] < self.position[1] + self.size[1] and d.height >= h:
                h = d.height + 1
        self.height = h

def deck(clist,pos,back):
    global cards
    cl = clist
    random.shuffle(cl)
    for dc in cl:
        cards.append(card(dc))
        cards[-1].position = pos[:]
        cards[-1].place()
        cards[-1].back = back

cards = []
deck([
    "h1","h2","h3","h4","h5","h6","h7","h8","h9","h10","hj","hq","hk"
    #"d1","d2","d3","d4","d5","d6","d7","d8","d9","d10","dj","dq","dk",
    #"c1","c2","c3","c4","c5","c6","c7","c8","c9","c10","cj","cq","ck",
    #"s1","s2","s3","s4","s5","s6","s7","s8","s9","s10","sj","sq","sk"
],[400,400],"2")

def animate(cards,select):
    screen.blit(board,[0,0])
    y = 0
    drawn = 0
    while drawn < len(cards):
        for d in cards:
            if d.height == y:
                if d.flipped:
                    screen.blit(pygame.transform.rotate(d.texture,-90 * d.rotation),d.position)
                else:
                    screen.blit(pygame.transform.rotate(pygame.image.load("graphics/back%s.png" % d.back),-90 * d.rotation),d.position)
                drawn += 1
        y += 1
    if magnify and select != None and select.flipped:
    	screen.blit(pygame.transform.rotate(select.magnified,-90 * select.rotation),[select.position[0] + select.size[0] / 2 - select.magsize[0] / 2,select.position[1] + select.size[1] / 2 - select.magsize[1] / 2])
    pygame.display.flip()

playing = True
mousedown = False
mouseposition = [0,0]
select = None
magnify = False
animate(cards,select)
while playing:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            playing = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mousedown = True
            h = -1
            select = None
            for d in cards:
                if d.position[0] < mouseposition[0] and d.position[0] + d.size[0] > mouseposition[0] and d.position[1] < mouseposition[1] and d.position[1] + d.size[1] > mouseposition[1] and d.height > h:
                    h = d.height
                    select = d
            if select != None:
                select.place()
                animate(cards,select)
        elif event.type == pygame.MOUSEBUTTONUP:
            mousedown = False
            select = None
            animate(cards,select)
        elif event.type == pygame.MOUSEMOTION:
            if mousedown and select != None:
                select.position[0] += event.pos[0] - mouseposition[0]
                select.position[1] += event.pos[1] - mouseposition[1]
                select.place()
                animate(cards,select)
            mouseposition = event.pos[:]
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                h = -1
                selec = None
                for d in cards:
                    if d.position[0] < mouseposition[0] and d.position[0] + d.size[0] > mouseposition[0] and d.position[1] < mouseposition[1] and d.position[1] + d.size[1] > mouseposition[1] and d.height > h:
                        h = d.height
                        selec = d
                if selec != None:
                    selec.flipped = not selec.flipped
                    animate(cards,select)
            elif event.key == pygame.K_s:
                h = -1
                selec = None
                for d in cards:
                    if d.position[0] < mouseposition[0] and d.position[0] + d.size[0] > mouseposition[0] and d.position[1] < mouseposition[1] and d.position[1] + d.size[1] > mouseposition[1] and d.height > h:
                        h = d.height
                        selec = d
                if selec != None:
                    selec.rotation += 1
                    if selec.rotation >= 4:
                        selec.rotation = 0
                    selec.size = [selec.size[1],selec.size[0]]
                    selec.magsize = [selec.magsize[1],selec.magsize[0]]
                    selec.position = [selec.position[0] + selec.size[1] / 2 - selec.size[0] / 2,selec.position[1] + selec.size[0] / 2 - selec.size[1] / 2]
                    selec.place()
                    animate(cards,select)
            elif event.key == pygame.K_d:
                j = raw_input("Name:")
                k = j.split("*")
                try:
                    if len(k) == 1:
                        cards.append(card(k[0]))
                        cards[-1].place()
                    else:
                        for d in range(int(k[1])):
                            cards.append(card(k[0]))
                            cards[-1].place()
                            if len(k) == 3:
                                cards[-1].back = k[2]
                except:
                    print "Could not find card!"
                animate(cards,select)
            elif event.key == pygame.K_l:
                magnify = not magnify
            elif event.key == pygame.K_f:
                h = -1
                selec = None
                for d in cards:
                    if d.position[0] < mouseposition[0] and d.position[0] + d.size[0] > mouseposition[0] and d.position[1] < mouseposition[1] and d.position[1] + d.size[1] > mouseposition[1] and d.height > h:
                        h = d.height
                        selec = d
                if selec != None and selec.flipped:
                    view = True
                    animate(cards,select)
                    screen.blit(selec.magnified,[screensize[0] / 2 - selec.magsize[0] / 2,screensize[1] / 2 - selec.magsize[1] / 2])
                    pygame.display.flip()
                    while view:
                        for event in pygame.event.get():
                            if event.type == pygame.QUIT:
                                playing = False
                                view = False
                            elif event.type == pygame.KEYDOWN:
                                if event.key == pygame.K_f:
                                    view = False
                    animate(cards,select)
            elif event.key == pygame.K_g:
                h = -1
                selec = None
                for d in cards:
                    if d.position[0] < mouseposition[0] and d.position[0] + d.size[0] > mouseposition[0] and d.position[1] < mouseposition[1] and d.position[1] + d.size[1] > mouseposition[1] and d.height > h:
                        h = d.height
                        selec = d
                if selec != None:
                    cards.remove(selec)
                    animate(cards,select)
            elif event.key == pygame.K_h:
                shuffle = []
                for d in cards[:]:
                    if d.position[0] < mouseposition[0] and d.position[0] + d.size[0] > mouseposition[0] and d.position[1] < mouseposition[1] and d.position[1] + d.size[1] > mouseposition[1]:
                        cards.remove(d)
                        shuffle.append(d)
                random.shuffle(shuffle)
                for de in shuffle:
                    cards.append(de)
                    cards[-1].place()
                animate(cards,select)
pygame.quit()
