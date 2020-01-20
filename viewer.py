import sys
import moderngl as mgl
from PyQt5 import QtWidgets

from util import *
from camera import Camera
from scene import Scene


class ViewerWidget(QModernGLWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.scene = None
        self.last_x = None
        self.last_y = None

        self.mouse_middle_pressed = False
        self.shift_pressed = False

    def init(self):
        self.ctx.viewport = self.viewport
        self.scene = Scene(self.ctx)
        self.ctx_init()

    def render(self):
        self.screen.use()
        self.scene.clear()
        vp = self.scene.camera.view_proj()
        self.scene.draw(vp)
    
    def ctx_init(self):
        self.ctx.enable(mgl.DEPTH_TEST)
        self.ctx.enable(mgl.CULL_FACE)

    def mousePressEvent(self, event):
        self.last_x = event.x()
        self.last_y = event.y()
        if event.button() == 4:
            self.mouse_middle_pressed = True
        self.update()

    def mouseReleaseEvent(self, event):
        self.last_x = None
        self.last_y = None
        if event.button() == 4:
            self.mouse_middle_pressed = False
        self.update()

    def mouseMoveEvent(self, event):
        dx = event.x() - self.last_x
        dy = event.y() - self.last_y
        self.last_x = event.x()
        self.last_y = event.y()
        if self.mouse_middle_pressed == True:
            if self.shift_pressed == False:
                self.scene.camera.orbit(dx, dy)
            else:
                self.scene.camera.pan(dx, dy)
        self.update()
    
    def wheelEvent(self, event):
        offset = event.angleDelta().y() / 120
        self.scene.camera.dolly(offset)
        self.update()
    
    def resizeEvent(self, event):
        width = event.size().width()
        height = event.size().height()
        if width > height:
            self.viewport = (int((width - height) / 2), 0, height, height)
        else:
            self.viewport = (0, int((height - width) / 2), width, width)
        if hasattr(self, 'ctx') and hasattr(self.ctx, 'viewport'):
            self.ctx.viewport = self.viewport

    def press_shift(self):
        self.shift_pressed = True

    def release_shift(self):
        self.shift_pressed = False
    
    def load_mesh(self, path):
        self.scene.load_mesh(path)
        self.update()

    def release_mesh(self):
        self.scene.release_mesh()
        self.update()


def main():
    app = QtWidgets.QApplication(sys.argv)
    widget = ViewerWidget()
    widget.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()