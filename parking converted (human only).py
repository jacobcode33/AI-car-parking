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

for obstacles in range (8, 15):
     hyp = 20 # the physical size of cars and obstacles (not to be confused with zoom)
     ox = []
     oy = []
     carx = random.randint (-round(screenwidth/3), round(screenwidth/3))
     cary = random.randint (-(screenheight/3), (screenheight/3))
     startx= carx
     starty = cary
     cara = random.randint (0, 359)
     speed = 0
     acceleration = 0.08
     sensitivity = 0.65
     count =500

     for i in range (0, obstacles):
          a = random.randint(0, 359)
          okay = False
          while okay == False:
               okay = True
               x = random.randint (-round(screenwidth/2), round(screenwidth/2))
               y = random.randint (-round(screenheight/2), round(screenheight/2))
               if (math.sqrt((x-carx)**2 + (y-cary)**2)) < hyp*2:
                    okay = False
               for o in range (0, len(ox)):
                    if (math.sqrt((ox[o]-x)**2 + (oy[o]-y)**2)) < hyp*1.25:
                         okay = False
          for e in range (0, 4):
               ox.append (x+hyp*math.cos(math.radians(a+e*90)))
               oy.append (y+hyp*math.sin(math.radians(a+e*90)))

     def crashed(crashs):
          global speed
          global crash
          global carx
          global cary
          global cara

          speed = crashs*-0.1
          carx = carx + math.cos(math.radians(cara-45)) * -crashs
          cary = cary + math.sin(math.radians(cara-45)) * -crashs

     def draw():
          global carx
          global cary
          global cara
          for i in range (0, obstacles):
               obstacle = Polygon(Point(ox[(4*i)], oy[(4*i)]), Point(ox[(4*i)+1], oy[(4*i)+1]), Point(ox[(4*i)+2], oy[(4*i)+2]), Point(ox[(4*i)+3], oy[(4*i)+3]))
               obstacle.draw(canvas)
          car = Polygon (Point(carx+(hyp*math.cos(math.radians(cara))),(cary+(hyp*math.sin(math.radians(cara))))), Point(carx+(hyp*math.cos(math.radians(cara+90))),(cary+(hyp*math.sin(math.radians(cara+90))))), Point(carx+(hyp*math.cos(math.radians(cara+180))),(cary+(hyp*math.sin(math.radians(cara+180))))), Point(carx+(hyp*(math.cos(math.radians(cara+270)))),(cary+(hyp*(math.sin(math.radians(cara+270)))))))
          car.setFill(color_rgb(0,0, 0))
          car.draw(canvas)
          timer = Text(Point(round(screenwidth/2)-30 , round(screenheight/2)-20), str(count))
          timer.draw(canvas)
          canvas.update()
          for item in canvas.items[:]:
               item.undraw()

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

     def confirm():
          global w
          global a
          global s
          global d
          global r
          global speed
          global carx
          global cary
          global accelleration
          global sensitivity
          global cara
          
          if w == True:
               speed = speed + acceleration
          if s == True:
               speed = speed*0.8
          if r == True:
               speed = speed - acceleration*0.5
          if a == True:
               cara = cara + speed * sensitivity
          if d == True:
               cara = cara - speed * sensitivity
          speed = speed *0.98
          carx = carx + math.cos(math.radians(cara-45)) * speed
          cary = cary + math.sin(math.radians(cara-45)) * speed

     def check():
          global crash
          global carx
          global cary
          global cara

          # if it touches screen edges
          x1 = (carx+(hyp*math.cos(math.radians(cara))))
          x2 = (carx+(hyp*math.cos(math.radians(cara+90))))
          x3 = (carx+(hyp*math.cos(math.radians(cara+180))))
          x4 = (carx+(hyp*math.cos(math.radians(cara+270))))
          y1 = (cary+(hyp*math.sin(math.radians(cara))))
          y2 = (cary+(hyp*math.sin(math.radians(cara+90))))
          y3 = (cary+(hyp*math.sin(math.radians(cara+180))))
          y4 = (cary+(hyp*math.sin(math.radians(cara+270))))
          
          if x1 < (screenwidth/-2) or x2 < (screenwidth/-2) or x3 < (screenwidth/-2) or x4 < (screenwidth/-2) or x1 > (screenwidth/2) or x2 > (screenwidth/2) or x3 > (screenwidth/2) or x4 > (screenwidth/2):
               crash = 3
               crashspeed = speed
          elif y1 < (screenheight/-2) or y2 < (screenheight/-2) or y3 < (screenheight/-2) or y4 < (screenheight/-2) or y1 > (screenheight/2) or y2 > (screenheight/2) or y3 > (screenheight/2) or y4 > (screenheight/2):
               crash = 3
               crashspeed = speed
          for o in range (0, len(ox)):
                    
               if (math.sqrt((ox[o]-carx)**2 + (oy[o]-cary)**2)) < hyp*1.5:
                     # if the detected corner is inside the car
                    x1 = (carx+(hyp*math.cos(math.radians(cara))))
                    x2 = (carx+(hyp*math.cos(math.radians(cara+90))))
                    x3 = (carx+(hyp*math.cos(math.radians(cara+180))))
                    x4 = (carx+(hyp*math.cos(math.radians(cara+270))))
                    y1 = (cary+(hyp*math.sin(math.radians(cara))))
                    y2 = (cary+(hyp*math.sin(math.radians(cara+90))))
                    y3 = (cary+(hyp*math.sin(math.radians(cara+180))))
                    y4 = (cary+(hyp*math.sin(math.radians(cara+270))))
                    
                    s1 = ((ox[o] - x1)*(y2 - y1)) - ((oy[o] - y1)*(x2 - x1)) # left side
                    s2 = ((ox[o] - x3)*(y4 - y3)) - ((oy[o] - y3)*(x4 - x3)) # right side
                    s3 = ((ox[o] - x2)*(y3 - y2)) - ((oy[o] - y2)*(x3 - x2)) # front side
                    s4 = ((ox[o] - x4)*(y1 - y4)) - ((oy[o] - y4)*(x1 - x4)) # back side
                    if s1 < 0 and s2 < 0 and s3 < 0 and s4 < 0:
                         crash = 1
                         crashspeed = speed

                    # if any car corners are inside the obstacle
                    obno = math.trunc(o / 4)
                    for u in range (0, 4):
                         cornerx = (carx+(hyp*math.cos(math.radians(cara + (u*90)))))
                         cornery = (cary+(hyp*math.sin(math.radians(cara + (u*90)))))
                         
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
                              crashspeed = speed
                              
          if crash != False:
               crashed(speed)
                              
     while count > 0:
          crash = False
          time.sleep (0.01)
          draw()
          humanchoose()
          check()
          confirm()
