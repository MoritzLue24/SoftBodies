import math
import threading
import pygame


class Utils:
    @staticmethod
    def pointOnLine(a, b, c, epsilon):
        def _is_zero( val ):
            return -epsilon < val < epsilon

        x1 = a.x - b.x
        x2 = c.x - b.x
        y1 = a.y - b.y
        y2 = c.y - b.y

        if _is_zero(x1) and _is_zero(y1):
            return _is_zero(x2) and _is_zero(y2)

        if _is_zero(x1):
            m2 = y2 * 1.0 / y1
            return _is_zero(x2) and 0 <= m2 <= 1
        elif _is_zero(y1):
            m1 = x2 * 1.0 / x1
            return _is_zero(y2) and 0 <= m1 <= 1
        else:
            m1 = x2 * 1.0 / x1
            if m1 < 0 or m1 > 1:
                return False
            m2 = y2 * 1.0 / y1
            return _is_zero(m2 - m1)

    @staticmethod
    def pointOnCircle(circlePos, pt1, radius: float, hitboxX: float=0, hitboxY: float=0):
        xC, x1 = circlePos.x, pt1.x
        yC, y1 = circlePos.y, pt1.y

        onCircleX = (x1 < xC + radius + hitboxX) and (x1 > xC - radius - hitboxX)
        onCircleY = (y1 < yC + radius + hitboxY) and (y1 > yC - radius - hitboxY)

        return onCircleX and onCircleY

    @staticmethod
    def getLineLength(pt1, pt2):
        x1, x2 = pt1.x, pt2.x
        y1, y2 = pt1.y, pt2.y

        return math.sqrt((x2-x1)**2 + (y2-y1)**2)

    @staticmethod
    def thread(fn):
        def run(*k, **kw):
            t = threading.Thread(target=fn, args=k, kwargs=kw)
            t.start()
            return t
        return run

    @staticmethod
    def getCirclePoint(centerPos: pygame.Vector2, r: float, angle: float):
        return pygame.Vector2(centerPos.x + r * math.cos(angle), centerPos.y + r * math.sin(angle))
