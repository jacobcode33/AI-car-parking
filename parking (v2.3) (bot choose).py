from graphics import *
import time
import math
import keyboard
import random
import csv

screenwidth = 600
screenheight = 600
canvas = GraphWin("canvas", screenwidth, screenheight, autoflush = False)
canvas.setBackground (color_rgb(255, 255, 255))
canvas.setCoords(-(screenwidth/2),-(screenheight/2),(screenwidth/2),(screenheight/2))

def makename():
     global name
     namelist = open ("surnames.csv", "rt", newline = "")
     data = csv.reader (namelist, delimiter=',')
     for row in data:
          if random.randint(1,2) == 1:
               prefix = "Mr"
          elif random.randint(1,2) == 1:
               prefix = "Mrs"
          elif random.randint(1,3) == 1:
               prefix = "Miss"
          elif random.randint(1,3) == 1:
               prefix = "Sir"
          elif random.randint(1,3) == 1:
               prefix = "Lady"
          elif random.randint(1,3) == 1:
               prefix = "Master"
          else:
               prefix = "Lord"
     name =  (prefix+" "+ (row[random.randint(0,2154)]).title())

def intersect(x1, x2, x3, x4, y1, y2, y3, y4):
     global px3
     global py3
     px1 = (((x1*y2) - (y1*x2)) * (x3-x4)) - ((x1-x2) * ((x3*y4) - (y3*x4)))
     px2 = ((x1-x2) * (y3-y4)) - ((y1-y2) * (x3-x4))
     if px2 == 0:
          px2 = 0.000001
     px3 = px1/px2

     py1 = (((x1*y2) - (y1*x2)) * (y3-y4)) - ((y1-y2) * ((x3*y4) - (y3*x4)))
     py2 = ((x1-x2) * (y3-y4)) - ((y1-y2) * (x3-x4))
     if py2 == 0:
          py2 = 0.000001
     py3 = py1/py2

def sense(who):
     #(math.sqrt((hyp**2)/2))

     sensors[4] = math.sqrt((goalx-carx[who])**2 + (goaly-cary[who])**2)
     sensors[5] = (cara[who] - 45 - (math.degrees(math.atan2((goaly - cary[who]),(goalx - carx[who])))))%360
     if sensors[5] > 180:
          sensors[5] = sensors[5] - 360

     for e in range (0, 4):
          if e == 0:
               owl = -90
               red = -hyp
          if e == 1:
               owl = -45
               red = -(math.sqrt((hyp**2)/2))
          if e ==2:
               owl = 0
               red = -hyp
          if e == 3:
               owl = 135
               red = -(math.sqrt((hyp**2)/2))

          x1 = carx[who]
          x2 = carx[who] + math.cos(math.radians(cara[who]+owl)) * hyp
          y1 = cary[who]
          y2 = cary[who] + math.sin(math.radians(cara[who]+owl)) * hyp

          # top or bottom
          x3 = -1
          x4 = 1
          if ((cara[who]+owl)%360) < 180:
               y3 = (screenheight/2)
               y4 = (screenheight/2)
          else:
               y3 = -(screenheight/2)
               y4 = -(screenheight/2)
          intersect(x1, x2, x3, x4, y1, y2, y3, y4)
          distance = red + (math.sqrt(((carx[who]-px3)**2) + ((cary[who]-py3)**2)))
          if distance < 0:
               distance = 0
          if distance < sensors[e]:
               sensors[e] = distance

          # left or right
          y3 = -1
          y4 = 1
          if ((cara[who]+owl+90)%360) < 180:
               x3 = (screenwidth/2)
               x4 = (screenwidth/2)
          else:
               x3 = -(screenwidth/2)
               x4 = -(screenwidth/2)
          intersect(x1, x2, x3, x4, y1, y2, y3, y4)
          distance = red + (math.sqrt(((carx[who]-px3)**2) + ((cary[who]-py3)**2)))
          if distance < 0:
               distance = 0
          if distance < sensors[e]:
               sensors[e] = distance
               
          # obstacles
          for o in range (0, obstacles):
               for i in range (0, 4):
                    x3 = ox[(4*o)+(i%4)]
                    x4 = ox[(4*o)+((i+1)%4)]
                    y3 = oy[(4*o)+(i%4)]
                    y4 = oy[(4*o)+((i+1)%4)]
                    intersect(x1, x2, x3, x4, y1, y2, y3, y4)
                    # needs to check if the point is between the max possible xy and the min possible xy
                    # next needs to check that it isn't looking backwards
                    legit = False
                    if ((px3 <= x3 and px3 >= x4) or (px3 <= x4 and px3 >= x3)) and ((py3 <= y3 and py3 >= y4) or (py3 <= y4 and py3 >= y3)):
                         legit = True
                    if ((px3 - (carx[who] + math.cos(math.radians(cara[who]+owl+90))))*((cary[who] + math.sin(math.radians(cara[who]+owl-90))) - (cary[who] + math.sin(math.radians(cara[who]+owl+90))))) - ((py3 - (cary[who] + math.sin(math.radians(cara[who]+owl+90))))*((carx[who] + math.cos(math.radians(cara[who]+owl-90))) - (carx[who] + math.cos(math.radians(cara[who]+owl+90))))) > 0:
                         legit = False
                    distance = red + (math.sqrt(((carx[who]-px3)**2) + ((cary[who]-py3)**2)))
                    if distance < 0:
                         distance = 0
                    if distance < sensors[e] and legit == True:
                         sensors[e] = distance
     for i in range (0,5):
          sensors[i] = sensors[i] / 500
     sensors[5] = sensors[5]/100

def crashed(crashs, who):
     global speed
     global crash
     global score

     speed[who] = crashs*-0.1
     carx[who] = carx[who] + math.cos(math.radians(cara[who]-45)) * -crashs
     cary[who] = cary[who] + math.sin(math.radians(cara[who]-45)) * -crashs

     if crash == 1:
          score[who] = score[who] - (crashs ** 2)*10
     if crash == 2:
          score[who] = score[who] - (crashs ** 2)*10
     if crash == 3:
          score[who] = score[who] - (crashs ** 2)*10

def draw():
     global carx
     global cary
     global cara
     global goalx
     global goaly
     global goala
     for i in range (0, obstacles):
          obstacle = Polygon(Point(ox[(4*i)], oy[(4*i)]), Point(ox[(4*i)+1], oy[(4*i)+1]), Point(ox[(4*i)+2], oy[(4*i)+2]), Point(ox[(4*i)+3], oy[(4*i)+3]))
          obstacle.draw(canvas)
     for i in range (0, bots):
          car = Polygon (Point(carx[i]+(hyp*math.cos(math.radians(cara[i]))),(cary[i]+(hyp*math.sin(math.radians(cara[i]))))), Point(carx[i]+(hyp*math.cos(math.radians(cara[i]+90))),(cary[i]+(hyp*math.sin(math.radians(cara[i]+90))))), Point(carx[i]+(hyp*math.cos(math.radians(cara[i]+180))),(cary[i]+(hyp*math.sin(math.radians(cara[i]+180))))), Point(carx[i]+(hyp*(math.cos(math.radians(cara[i]+270)))),(cary[i]+(hyp*(math.sin(math.radians(cara[i]+270)))))))
          car.setFill(color_rgb(0,i*20,0))
          car.draw(canvas)
     goal = Polygon (Point(goalx+(hyp*math.cos(math.radians(goala))),(goaly+(hyp*math.sin(math.radians(goala))))), Point(goalx+(hyp*math.cos(math.radians(goala+90))),(goaly+(hyp*math.sin(math.radians(goala+90))))), Point(goalx+(hyp*math.cos(math.radians(goala+180))),(goaly+(hyp*math.sin(math.radians(goala+180))))), Point(goalx+(hyp*(math.cos(math.radians(goala+270)))),(goaly+(hyp*(math.sin(math.radians(goala+270)))))))
     goal.setOutline(color_rgb(150,0, 0))
     goal.setWidth(3)
     goal.draw(canvas)
     timer = Text(Point(round(screenwidth/2)-30 , round(screenheight/2)-20), str(count))
     timer.draw(canvas)
     points =  Text(Point(0 , round(screenheight/2)-20), str(round(max(score))))
     points.draw(canvas)
     canvas.update()
     for item in canvas.items[:]:
          item.undraw()

def sigmoid(value):
     e = 2.718
     return (1-(1 / (1 + e**(-value/200))))*2

def botchoose(who):
     global w
     global a
     global s
     global d
     global r

     weight = []
     bias = []
     for i in range (0, 36):
          weight.append (1/(i+1))
     for i in range (0,6):
          bias.append (0)

     w = bias[0]
     s = bias[1]
     r = bias[2]
     a = bias[3]
     d = bias[4]

     for i in range (0, 6):
          w = w+ (sensors[i] * weight[i])
          s = s+ (sensors[i] * weight[i+5])
          r = r+ (sensors[i] * weight[i+10])
          a = a+ (sensors[i] * weight[i+15])
          d = d+ (sensors[i] * weight[i+20])

     w = sigmoid(w*200)
     s = sigmoid(s*200)
     r = sigmoid(r*200)
     a = sigmoid(a*200)
     d = sigmoid(d*200)

     if w > 0.5:
          w = True
     if s > 0.5:
          s = True
     if r > 0.5:
          r =True
     if a > 0.5:
          a = True
     if d > 0.5:
          d = True
     

def humanchoose():
     global w
     global a
     global s
     global d
     global r

     w = False
     s = False
     r = False
     a = False
     d = False
     if keyboard.is_pressed("w"):
          w = True
     if keyboard.is_pressed("s"):
          s = True
     if keyboard.is_pressed("r"):
          r = True
     if keyboard.is_pressed("a"):
          a = True
     if keyboard.is_pressed("d"):
          d = True

def confirm(who):
     global w
     global a
     global s
     global d
     global r
     global accelleration
     global sensitivity
     
     if w == True:
          speed[who] = speed[who] + acceleration
     if s == True:
          speed[who] = speed[who]*(1-(2.5*acceleration))
     if r == True:
          speed[who] = speed[who] - acceleration*0.5
     if a == True:
          cara[who] = cara[who] + speed[who] * sensitivity
     if d == True:
          cara[who] = cara[who] - speed[who] * sensitivity
     speed[who] = speed[who] * (1-(acceleration/ 4))
     carx[who] = carx[who] + math.cos(math.radians(cara[who]-45)) * speed[who]
     cary[who] = cary[who] + math.sin(math.radians(cara[who]-45)) * speed[who]

def check(who):
     global crash
     global crashspeed

     # if it touches screen edges
     x1 = (carx[who]+(hyp*math.cos(math.radians(cara[who]))))
     x2 = (carx[who]+(hyp*math.cos(math.radians(cara[who]+90))))
     x3 = (carx[who]+(hyp*math.cos(math.radians(cara[who]+180))))
     x4 = (carx[who]+(hyp*math.cos(math.radians(cara[who]+270))))
     y1 = (cary[who]+(hyp*math.sin(math.radians(cara[who]))))
     y2 = (cary[who]+(hyp*math.sin(math.radians(cara[who]+90))))
     y3 = (cary[who]+(hyp*math.sin(math.radians(cara[who]+180))))
     y4 = (cary[who]+(hyp*math.sin(math.radians(cara[who]+270))))
     
     if x1 < (screenwidth/-2) or x2 < (screenwidth/-2) or x3 < (screenwidth/-2) or x4 < (screenwidth/-2) or x1 > (screenwidth/2) or x2 > (screenwidth/2) or x3 > (screenwidth/2) or x4 > (screenwidth/2):
          crash = 3
          crashspeed = speed[who]
     elif y1 < (screenheight/-2) or y2 < (screenheight/-2) or y3 < (screenheight/-2) or y4 < (screenheight/-2) or y1 > (screenheight/2) or y2 > (screenheight/2) or y3 > (screenheight/2) or y4 > (screenheight/2):
          crash = 3
          crashspeed = speed[who]
     for o in range (0, len(ox)):
               
          if (math.sqrt((ox[o]-carx[who])**2 + (oy[o]-cary[who])**2)) < hyp*1.5:
                # if the detected corner is inside the car
               x1 = (carx[who]+(hyp*math.cos(math.radians(cara[who]))))
               x2 = (carx[who]+(hyp*math.cos(math.radians(cara[who]+90))))
               x3 = (carx[who]+(hyp*math.cos(math.radians(cara[who]+180))))
               x4 = (carx[who]+(hyp*math.cos(math.radians(cara[who]+270))))
               y1 = (cary[who]+(hyp*math.sin(math.radians(cara[who]))))
               y2 = (cary[who]+(hyp*math.sin(math.radians(cara[who]+90))))
               y3 = (cary[who]+(hyp*math.sin(math.radians(cara[who]+180))))
               y4 = (cary[who]+(hyp*math.sin(math.radians(cara[who]+270))))
               
               s1 = ((ox[o] - x1)*(y2 - y1)) - ((oy[o] - y1)*(x2 - x1)) # left side
               s2 = ((ox[o] - x3)*(y4 - y3)) - ((oy[o] - y3)*(x4 - x3)) # right side
               s3 = ((ox[o] - x2)*(y3 - y2)) - ((oy[o] - y2)*(x3 - x2)) # front side
               s4 = ((ox[o] - x4)*(y1 - y4)) - ((oy[o] - y4)*(x1 - x4)) # back side
               if s1 < 0 and s2 < 0 and s3 < 0 and s4 < 0:
                    crash = 1
                    crashspeed = speed[who]

               # if any car corners are inside the obstacle
               obno = math.trunc(o / 4)
               for u in range (0, 4):
                    cornerx = (carx[who]+(hyp*math.cos(math.radians(cara[who] + (u*90)))))
                    cornery = (cary[who]+(hyp*math.sin(math.radians(cara[who] + (u*90)))))
                    
                    x1 = ox[4*obno]
                    x2 = ox[4*obno+1]
                    x3 = ox[4*obno+2]
                    x4 = ox[4*obno+3]
                    y1 = oy[4*obno]
                    y2 = oy[4*obno+1]
                    y3 = oy[4*obno+2]
                    y4 = oy[4*obno+3]

                    s1 = ((cornerx - x1)*(y2 - y1)) - ((cornery - y1)*(x2 - x1)) # left side       12
                    s2 = ((cornerx - x3)*(y4 - y3)) - ((cornery - y3)*(x4 - x3)) # right side     34
                    s3 = ((cornerx - x2)*(y3 - y2)) - ((cornery - y2)*(x3 - x2)) # front side     23
                    s4 = ((cornerx - x4)*(y1 - y4)) - ((cornery - y4)*(x1 - x4)) # back side      14

                    if s1 < 0 and s2 < 0 and s3 < 0 and s4 < 0:
                         crash = 2
                         crashspeed = speed[who]
                         
     if crash != False:
          crashed(crashspeed, who)

scores = []
name = ""
hyp = 50
bots = 1
for i in range (0, bots):
     scores.append (0)
for obstacles in range (0, 15):
     s1 = 0
     s2 = 0
     s3 = 0
     s4 = 0
     s5 = 0
     ox = []
     oy = []
     carx = []
     cary = []
     cara = []
     speed = []
     score = []
     startx= (random.randint (-round(screenwidth/3), round(screenwidth/3)))
     starty = (random.randint (-round(screenheight/3), round(screenheight/3)))
     starta = (random.randint(0, 359))
     for i in range (0, bots):
          carx.append (startx)
          cary.append (starty)
          cara.append (starta)
          speed.append (0)
          score.append (0)
     acceleration = 0.08
     sensitivity = 0.65
     count = 500

     okay = False
     while okay == False:
          okay = True
          goalx = random.randint (-round(screenwidth/2.5), round(screenwidth/2.5))
          goaly = random.randint (-round(screenheight/2.5), round(screenheight/2.5))
          goala = random.randint (0, 359)
          if (math.sqrt((goalx-startx)**2 + (goaly-starty)**2)) < hyp*3:
               okay = False

     for i in range (0, obstacles):
          a = random.randint(0, 359)
          okay = False
          while okay == False:
               okay = True
               x = random.randint (-round(screenwidth/2), round(screenwidth/2))
               y = random.randint (-round(screenheight/2), round(screenheight/2))
               if (math.sqrt((x-startx)**2 + (y-starty)**2)) < hyp*2:
                    okay = False
               if (math.sqrt((x-goalx)**2 + (y-goaly)**2)) < hyp*2:
                    okay = False
               for o in range (0, len(ox)):
                    if (math.sqrt((ox[o]-x)**2 + (oy[o]-y)**2)) < hyp*1.25:
                         okay = False
          for e in range (0, 4):
               ox.append (x+hyp*math.cos(math.radians(a+e*90)))
               oy.append (y+hyp*math.sin(math.radians(a+e*90)))

                              
     while count > 0:
          who = 0
          count = count - 1
          #time.sleep (0.01)
          draw()
          while who < bots:
               crash = False
               sensors = [9999, 9999, 9999, 9999, 9999, 9999]
               sense(who)
               botchoose(who)
               #humanchoose()
               check(who)
               confirm(who)
               who = who + 1

     for i in range(0, bots):
          moved = (math.sqrt((goalx-startx)**2 + (goaly-starty)**2)) - (math.sqrt((goalx-carx[i])**2 + (goaly-cary[i])**2))
          score[i] = (score[i]+moved)
          scores[i] = scores[i] + score[i]
          draw()
     time.sleep (0.5)

print (scores)
