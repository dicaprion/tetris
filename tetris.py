import sys
from shape import *
from collections import defaultdict
from PyQt5.QtWidgets import QMainWindow, QFrame, QDesktopWidget, QApplication, QMessageBox, QPushButton,  QTableWidget,\
    QTableWidgetItem, QInputDialog
from PyQt5.QtMultimedia import QSound
from PyQt5.QtCore import *
from PyQt5.QtGui import *

index = 0
removed = 0
x = 280
y = 580
boardWidth = 10
boardHeight = 22
highscoreList = defaultdict()
background = QSound("background1.wav")
line = QSound("line.wav")
drop = QSound("drop.wav")
clap = QSound("clap.wav")


class Highscore(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.initUI()

    def initUI(self):
        self.setWindowIcon(QIcon('icon.png'))
        self.table = QTableWidget(self)
        self.table.setColumnCount(2)
        self.table.setRowCount(10)
        self.table.move(100, 100)
        self.table.resize(280, 280)
        self.table.setColumnWidth(0, 95)
        self.table.setHorizontalHeaderLabels(["Player", "Score"])

        self.fillTable()

        buttonExit = QPushButton('return', self)
        buttonExit.resize(250, 75)
        buttonExit.move(117, 390)
        buttonExit.clicked.connect(self.close)

        self.resize(480, 480)
        self.center_window()
        self.show()

    def center_window(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def fillTable(self):
        i = 0
        set_names = set()
        sorted_list = sorted(highscoreList.values(), reverse=True)
        for value in sorted_list:
            for key in highscoreList.keys():
                if highscoreList[key] == value and key not in set_names:
                    set_names.add(key)
                    self.table.setItem(i, 0, QTableWidgetItem(key))
                    self.table.setItem(i, 1, QTableWidgetItem(str(value)))
                    i += 1


class PopupMap(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.initUI()

    def initUI(self):
        self.setWindowIcon(QIcon('icon.png'))
        buttonGame = QPushButton('10x22', self)
        buttonGame.resize(250, 75)
        buttonGame.move(117, 50)
        buttonGame.clicked.connect(self.on_click1)

        buttonTable = QPushButton('32x20', self)
        buttonTable.resize(250, 75)
        buttonTable.move(117, 150)
        buttonTable.clicked.connect(self.on_click2)

        buttonExit = QPushButton('40x40', self)
        buttonExit.resize(250, 75)
        buttonExit.move(117, 250)
        buttonExit.clicked.connect(self.on_click3)

        buttonExit = QPushButton('return', self)
        buttonExit.resize(250, 75)
        buttonExit.move(117, 350)
        buttonExit.clicked.connect(self.close)

        self.resize(480, 480)
        self.center_window()
        self.show()

    def center_window(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def startTertis(self):
        self.dialog = Tetris()
        self.dialog.show()

    def on_click1(self):
        Board.Width = 10
        Board.Height = 22
        Tetris.Width = 280
        Tetris.Height = 580
        self.startTertis()

    def on_click2(self):
        Board.Width = 32
        Board.Height = 20
        Tetris.Width = 680
        Tetris.Height = 480
        self.startTertis()

    def on_click3(self):
        Board.Width = 40
        Board.Height = 40
        Tetris.Width = 880
        Tetris.Height = 880
        self.startTertis()


class Popup(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.initUI()

    def initUI(self):
        self.setWindowIcon(QIcon('icon.png'))
        buttonGame = QPushButton('New Game', self)
        buttonGame.resize(250, 75)
        buttonGame.move(117, 100)
        buttonGame.clicked.connect(self.on_click1)

        buttonTable = QPushButton('Highscore table', self)
        buttonTable.resize(250, 75)
        buttonTable.move(117, 200)
        buttonTable.clicked.connect(self.on_click2)

        buttonExit = QPushButton('Exit', self)
        buttonExit.resize(250, 75)
        buttonExit.move(117, 300)
        buttonExit.clicked.connect(self.close)

        self.resize(480, 480)
        self.center_window()
        self.show()

    def center_window(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def on_click1(self):
        self.dialog = PopupMap()
        self.dialog.show()

    def on_click2(self):
        self.dialog = Highscore()
        self.dialog.show()

    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Quit',
            "Are you sure to quit?", QMessageBox.Yes |
            QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()


class Tetris(QMainWindow):
    Width = x
    Height = y

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.tboard = Board(self)
        self.setCentralWidget(self.tboard)
        self.statusbar = self.statusBar()
        self.tboard.status[str].connect(self.statusbar.showMessage)
        self.tboard.start()
        self.resize(Tetris.Width, Tetris.Height)
        self.setWindowTitle('Tetris')
        self.setWindowIcon(QIcon('icon.png'))
        self.center_window()
        self.show()

    def center_window(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def closeEvent(self, event):
        global index
        global removed
        background.stop()
        self.tboard.pause()
        reply = QMessageBox.question(self, 'Save', "Do you want to save the score?",
                                     QMessageBox.Yes | QMessageBox.Cancel | QMessageBox.No)
        if reply == QMessageBox.Yes:
            text, ok = QInputDialog.getText(self, 'Input Dialog', 'Enter your name:')
            if ok:
                if str(text) in highscoreList.keys():
                    highscoreList[str(text) + str(index)] = removed
                    index += 1
                else:
                    highscoreList[str(text)] = removed
            else:
                highscoreList["Player"] = removed

            removed = 0
            event.accept()
        elif reply == QMessageBox.No:
            event.accept()
        else:
            event.ignore()
            self.tboard.pause()
            background.setLoops(100)
            background.play()


class Board(QFrame):
    status = pyqtSignal(str)
    Width = boardWidth
    Height = boardHeight

    def __init__(self, parent=None):
        super().__init__(parent)
        self.initBoard()

    def initBoard(self):
        self.timer = QBasicTimer()
        self.isWaitingAfterLine = False
        self.currentX = 0
        self.currentY = 0
        self.speed = 300
        self.number = 5
        self.numLinesRemoved = 0
        self.board = []
        self.setFocusPolicy(Qt.StrongFocus)
        self.isStarted = False
        self.isPaused = False
        self.clear()

    def start(self):
        if self.isPaused:
            return
        self.isStarted = True
        self.isWaitingAfterLine = False
        self.numLinesRemoved = 0
        self.clear()
        self.status.emit(str(self.numLinesRemoved))
        self.newBlock()
        self.timer.start(self.speed, self)
        background.setLoops(100)
        background.play()

    def pause(self):
        if not self.isStarted:
            return
        self.isPaused = not self.isPaused
        if self.isPaused:
            self.timer.stop()
            self.status.emit("Paused")
            background.stop()
        else:
            background.setLoops(100)
            background.play()
            self.timer.start(self.speed, self)
            self.status.emit(str(self.numLinesRemoved))
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        rect = self.contentsRect()
        boardTop = rect.bottom() - Board.Height * self.squareHeight()
        for i in range(Board.Height):
            for j in range(Board.Width):
                shape = self.shapeAt(j, Board.Height - i - 1)

                if shape != Tetrominoe.Empty:
                    self.drawSquare(painter,
                        rect.left() + j * self.squareWidth(),
                        boardTop + i * self.squareHeight(), shape)
        if self.curBlock.shape() != Tetrominoe.Empty:
            for i in range(4):
                x = self.currentX + self.curBlock.x(i)
                y = self.currentY - self.curBlock.y(i)
                self.drawSquare(painter, rect.left() + x * self.squareWidth(),
                    boardTop + (Board.Height - y - 1) * self.squareHeight(),
                    self.curBlock.shape())

    def keyPressEvent(self, event):
        if not self.isStarted or self.curBlock.shape() == Tetrominoe.Empty:
            super(Board, self).keyPressEvent(event)
            return
        key = event.key()
        if key == Qt.Key_P:
            self.pause()
            return
        if self.isPaused:
            return
        elif key == Qt.Key_Right:
            self.tryMove(self.curBlock, self.currentX + 1, self.currentY)
        elif key == Qt.Key_Left:
            self.tryMove(self.curBlock, self.currentX - 1, self.currentY)
        elif key == Qt.Key_Down:
            self.tryMove(self.curBlock.rotateRight(), self.currentX, self.currentY)
        elif key == Qt.Key_Up:
            self.tryMove(self.curBlock.rotateLeft(), self.currentX, self.currentY)
        elif key == Qt.Key_Space:
            self.dropDown()
        else:
            super(Board, self).keyPressEvent(event)

    def timerEvent(self, event):
        if event.timerId() == self.timer.timerId():
            if self.isWaitingAfterLine:
                self.isWaitingAfterLine = False
                self.newBlock()
            else:
                self.down()
        else:
            super(Board, self).timerEvent(event)

    def clear(self):
        for i in range(Board.Height * Board.Width):
            self.board.append(Tetrominoe.Empty)

    def dropDown(self):
        newY = self.currentY
        while newY > 0:
            if not self.tryMove(self.curBlock, self.currentX, newY - 1):
                break
            newY -= 1
        self.BlockDropped()

    def down(self):
        if not self.tryMove(self.curBlock, self.currentX, self.currentY - 1):
            self.BlockDropped()

    def BlockDropped(self):
        for i in range(4):
            x = self.currentX + self.curBlock.x(i)
            y = self.currentY - self.curBlock.y(i)
            self.setShapeAt(x, y, self.curBlock.shape())
        self.removeFullLines()
        if not self.isWaitingAfterLine:
            self.newBlock()
        drop.play()

    def shapeAt(self, x, y):
        return self.board[(y * Board.Width) + x]

    def setShapeAt(self, x, y, shape):
        self.board[(y * Board.Width) + x] = shape

    def squareWidth(self):
        return self.contentsRect().width() // Board.Width

    def squareHeight(self):
        return self.contentsRect().height() // Board.Height

    def removeFullLines(self):
        global removed
        count = 0
        toRemove = []
        for i in range(Board.Height):
            n = 0
            for j in range(Board.Width):
                if not self.shapeAt(j, i) == Tetrominoe.Empty:
                    n = n + 1
            if n == Board.Width:
                toRemove.append(i)
                toRemove.reverse()
        for m in toRemove:
            for k in range(m, Board.Height):
                for l in range(Board.Width):
                        self.setShapeAt(l, k, self.shapeAt(l, k + 1))
        count = count + len(toRemove)
        if count > 0:
            self.numLinesRemoved = self.numLinesRemoved + count
            removed = self.numLinesRemoved
            self.status.emit(str(self.numLinesRemoved))
            self.isWaitingAfterLine = True
            self.curBlock.setShape(Tetrominoe.Empty)
            line.play()
            if self.numLinesRemoved >= self.number:
                self.number = self.number + 5
                self.changeSpeed()
            self.update()

    def newBlock(self):
        self.curBlock = Shape()
        self.curBlock.setRandomShape()
        self.currentX = Board.Width // 2 + 1
        self.currentY = Board.Height - 1 + self.curBlock.minY()
        if not self.tryMove(self.curBlock, self.currentX, self.currentY):
            self.curBlock.setShape(Tetrominoe.Empty)
            self.timer.stop()
            self.isStarted = False
            background.stop()
            self.status.emit("Game over")

    def tryMove(self, newBlock, newX, newY):
        for i in range(4):
            x = newX + newBlock.x(i)
            y = newY - newBlock.y(i)
            if x < 0 or x >= Board.Width or y < 0 or y >= Board.Height:
                return False
            if self.shapeAt(x, y) != Tetrominoe.Empty:
                return False
        self.curBlock = newBlock
        self.currentX = newX
        self.currentY = newY
        self.update()
        return True

    def changeSpeed(self):
        if self.speed - 100 > 0:
            self.speed = self.speed - 100
            self.timer.start(self.speed, self)

    def drawSquare(self, painter, x, y, shape):
        colorTable = [0x000000, 0xCC6666, 0x66CC66, 0x6666CC,
                      0xCCCC66, 0xCC66CC, 0x66CCCC, 0xDAAA00]
        color = QColor(colorTable[shape])
        painter.fillRect(x + 1, y + 1, self.squareWidth() - 2,
            self.squareHeight() - 2, color)
        painter.setPen(color.lighter())
        painter.drawLine(x, y + self.squareHeight() - 1, x, y)
        painter.drawLine(x, y, x + self.squareWidth() - 1, y)
        painter.setPen(color.darker())
        painter.drawLine(x + 1, y + self.squareHeight() - 1,
            x + self.squareWidth() - 1, y + self.squareHeight() - 1)
        painter.drawLine(x + self.squareWidth() - 1,
            y + self.squareHeight() - 1, x + self.squareWidth() - 1, y + 1)


if __name__ == '__main__':
    app = QApplication([])
    menu = Popup()
    sys.exit(app.exec_())
