import sys
import ac
import acsys
import math

appWindow=0
appWidth = 200
appHeight = 350
drawScale = 0.5
load = [0] * 4
smooth = 0.9

def acMain(ac_version):
    global appWindow
    appWindow = ac.newApp("Load Distribution")
    ac.setSize(appWindow, appWidth, appHeight)
    ac.setTitle(appWindow, "Load Distribution")
    ac.drawBorder(appWindow, 0)
    ac.setIconPosition(appWindow, 0, -10000)
    ac.setBackgroundColor(appWindow, 0, 0, 0)
    ac.setBackgroundOpacity(appWindow, 0.4)
    ac.drawBackground(appWindow, 1)
    ac.addRenderCallback(appWindow, drawIndicator)
    return "Load Distribution"

def drawIndicator(deltaT):
    global appWindow
    ac.setBackgroundOpacity(appWindow, 0)
    
    load_new = ac.getCarState(0, acsys.CS.Load)
    for i in range(4):
        load[i] = load[i] * smooth + load_new[i] * (1 - smooth)
    circleScale = 0.006
    offsetX = drawScale * appWidth / 2
    offsetY = drawScale * appHeight / 2
    step = 10
    ac.glColor4f(1, 1, 1, 0.5)
    drawLine(-offsetX, +offsetX, -offsetY, -offsetY, 3)
    drawLine(-offsetX, +offsetX, +offsetY, +offsetY, 3)
    drawLine(-offsetX, -offsetX, -offsetY, +offsetY, 3)
    drawLine(+offsetX, +offsetX, -offsetY, +offsetY, 3)
    ac.glColor4f(1, 0, 0, 1)
    drawCircle(-offsetX, -offsetY, circleScale * load[0], 3) #FL
    drawCircle(+offsetX, -offsetY, circleScale * load[1], 3) #FR
    drawCircle(-offsetX, +offsetY, circleScale * load[2], 3) #RL
    drawCircle(+offsetX, +offsetY, circleScale * load[3], 3) #RR
    
    total_load = max(sum(load), 1000)
    wX = (load[0] + load[2] - load[1] - load[3]) / total_load
    wY = (load[0] + load[1] - load[2] - load[3]) / total_load
    ac.glColor4f(0, 0, 1, 1)
    drawCircle(-offsetX * wX, -offsetY * wY, circleScale * total_load / 4, 5)
    ac.glColor4f(0.3, 0.3, 1, 1)
    drawLine(-offsetX, +offsetX, -offsetY * wY, -offsetY * wY, 3)
    drawLine(-offsetX * wX, -offsetX * wX, -offsetY, +offsetY, 3)

def drawCircle(x, y, r, width = 1):
    step = 10
    x += appWidth / 2
    y += appHeight / 2
    for i in range(0, 360, step):
        ac.glBegin(3)
        ac.glVertex2f(x + r * math.cos(math.radians(i)), y + r * math.sin(math.radians(i)))
        ac.glVertex2f(x + r * math.cos(math.radians(i+step)), y + r * math.sin(math.radians(i+step)))
        ac.glVertex2f(x + (r + width) * math.cos(math.radians(i+step)), y + (r + width) * math.sin(math.radians(i+step)))
        ac.glVertex2f(x + (r + width) * math.cos(math.radians(i)), y + (r + width) * math.sin(math.radians(i)))
        ac.glVertex2f(x + r * math.cos(math.radians(i)), y + r * math.sin(math.radians(i)))
        ac.glEnd()

def drawLine(x1, x2, y1, y2, width = 1):
    dx = x2 - x1
    dy = y2 - y1
    L = math.sqrt(dx ** 2 + dy ** 2)
    dx /= L
    dy /= L
    x1 += appWidth / 2
    x2 += appWidth / 2
    y1 += appHeight / 2
    y2 += appHeight / 2
    for i in range(width):
        ac.glBegin(1)
        ac.glVertex2f(x1 - dy * i, y1 + dx * i)
        ac.glVertex2f(x2 - dy * i, y2 + dx * i)
        ac.glEnd()
