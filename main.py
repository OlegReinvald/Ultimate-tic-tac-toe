import sys
import json
from PyQt5.QtWidgets import (
    QApplication, QWidget, QGridLayout, QPushButton, QMessageBox, QVBoxLayout,
    QColorDialog, QHBoxLayout, QLabel, QFileDialog, QLineEdit, QSpacerItem, QSizePolicy, QMenuBar, QAction
)
from PyQt5.QtGui import QFont, QColor, QPixmap, QIcon
from PyQt5.QtCore import Qt


class UltimateTicTacToe(QWidget):
    def __init__(self):
        super().__init__()
        self.left_image_path = ''
        self.right_image_path = ''
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Ultimate Tic-Tac-Toe')
        self.main_layout = QHBoxLayout()
        self.setLayout(self.main_layout)


        self.left_image_layout = QVBoxLayout()
        self.main_layout.addLayout(self.left_image_layout)

        self.left_image_layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

        self.game_layout = QVBoxLayout()
        self.main_layout.addLayout(self.game_layout)

        self.right_image_layout = QVBoxLayout()
        self.main_layout.addLayout(self.right_image_layout)

        self.right_image_layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

        self.grid = QGridLayout()
        self.game_layout.addLayout(self.grid)

        self.buttons = [[QPushButton(self) for _ in range(9)] for _ in range(9)]
        self.mini_grids = [[QGridLayout() for _ in range(3)] for _ in range(3)]
        self.mini_grid_widgets = [[QWidget(self) for _ in range(3)] for _ in range(3)]

        for i in range(3):
            for j in range(3):
                mini_grid_widget = self.mini_grid_widgets[i][j]
                mini_grid_widget.setLayout(self.mini_grids[i][j])
                mini_grid_widget.setFixedSize(200, 200)
                self.grid.addWidget(mini_grid_widget, i, j)

        for i in range(9):
            for j in range(9):
                board_x, cell_x = divmod(i, 3)
                board_y, cell_y = divmod(j, 3)
                self.mini_grids[board_x][board_y].addWidget(self.buttons[i][j], cell_x, cell_y)
                self.buttons[i][j].setFixedSize(60, 60)
                self.buttons[i][j].clicked.connect(lambda _, x=i, y=j: self.buttonClicked(x, y))
                self.buttons[i][j].setEnabled(False)

        self.current_player = 'X'
        self.main_board = [[None for _ in range(3)] for _ in range(3)]
        self.sub_boards = [[[None for _ in range(3)] for _ in range(3)] for _ in range(9)]
        self.next_allowed_board = None
        self.X_color = QColor("Red")
        self.O_color = QColor("Blue")
        self.status_label = QLabel("Press 'Start Game' to begin", self)
        self.status_label.setFont(QFont("Arial", 16, QFont.Bold))
        self.game_layout.addWidget(self.status_label)

        self.createMenu()
        self.createImageSelection()

    def createMenu(self):
        self.menu_bar = QMenuBar(self)
        self.main_layout.setMenuBar(self.menu_bar)

        game_menu = self.menu_bar.addMenu('Game')
        settings_menu = self.menu_bar.addMenu('Settings')
        file_menu = self.menu_bar.addMenu('File')

        self.start_action = QAction('Start Game', self)
        self.start_action.triggered.connect(self.startGame)
        game_menu.addAction(self.start_action)

        self.reset_action = QAction('Reset Game', self)
        self.reset_action.setShortcut('R')
        self.reset_action.triggered.connect(self.resetGame)
        game_menu.addAction(self.reset_action)

        self.save_action = QAction('Save Game', self)
        self.save_action.setShortcut('Ctrl+S')
        self.save_action.triggered.connect(self.saveGame)
        file_menu.addAction(self.save_action)

        self.load_action = QAction('Load Game', self)
        self.load_action.setShortcut('Ctrl+L')
        self.load_action.triggered.connect(self.loadGame)
        file_menu.addAction(self.load_action)

        self.x_color_action = QAction('Select X Color', self)
        self.x_color_action.triggered.connect(self.selectXColor)
        settings_menu.addAction(self.x_color_action)

        self.o_color_action = QAction('Select O Color', self)
        self.o_color_action.triggered.connect(self.selectOColor)
        settings_menu.addAction(self.o_color_action)

    def createImageSelection(self):
        self.left_nickname_label = QLabel("X's Nickname:", self)
        self.left_image_layout.addWidget(self.left_nickname_label)

        self.left_nickname_edit = QLineEdit(self)
        self.left_image_layout.addWidget(self.left_nickname_edit)

        self.left_image_label = QLabel(self)
        self.left_image_label.setFixedSize(200, 300)
        self.left_image_label.setStyleSheet("border: 1px solid black")
        self.left_image_layout.addWidget(self.left_image_label)

        self.left_image_button = QPushButton("Select Left Image", self)
        self.left_image_button.clicked.connect(self.selectLeftImage)
        self.left_image_layout.addWidget(self.left_image_button)

        self.left_image_layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

        self.right_nickname_label = QLabel("O's Nickname:", self)
        self.right_image_layout.addWidget(self.right_nickname_label)

        self.right_nickname_edit = QLineEdit(self)
        self.right_image_layout.addWidget(self.right_nickname_edit)

        self.right_image_label = QLabel(self)
        self.right_image_label.setFixedSize(200, 300)
        self.right_image_label.setStyleSheet("border: 1px solid black")
        self.right_image_layout.addWidget(self.right_image_label)

        self.right_image_button = QPushButton("Select Right Image", self)
        self.right_image_button.clicked.connect(self.selectRightImage)
        self.right_image_layout.addWidget(self.right_image_button)

        self.right_image_layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))


    def selectLeftImage(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Select Image", "", "Images (*.png *.jpg *.jpeg *.bmp)")
        if file_name:
            self.left_image_path = file_name
            pixmap = QPixmap(file_name)
            self.left_image_label.setPixmap(pixmap.scaled(self.left_image_label.size(), Qt.KeepAspectRatio))

    def selectRightImage(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Select Image", "", "Images (*.png *.jpg *.jpeg *.bmp)")
        if file_name:
            self.right_image_path = file_name
            pixmap = QPixmap(file_name)
            self.right_image_label.setPixmap(pixmap.scaled(self.right_image_label.size(), Qt.KeepAspectRatio))
    def startGame(self):
        self.resetGame()
        self.highlightBoard()
        self.status_label.setText("Game Started! Player X's turn")


        self.left_nickname_edit.setEnabled(False)
        self.right_nickname_edit.setEnabled(False)
        self.right_image_button.setEnabled(False)
        self.left_image_button.setEnabled(False)
        self.start_action.setEnabled(False)
        self.x_color_action.setEnabled(False)
        self.o_color_action.setEnabled(False)
        self.save_action.setEnabled(True)

        self.left_nickname = self.left_nickname_edit.text()
        self.right_nickname = self.right_nickname_edit.text()

    def selectXColor(self):
        color = QColorDialog.getColor()
        if color.isValid():
            self.X_color = color

    def selectOColor(self):
        color = QColorDialog.getColor()
        if color.isValid():
            self.O_color = color

    def buttonClicked(self, x, y):
        board_x, cell_x = divmod(x, 3)
        board_y, cell_y = divmod(y, 3)
        board_index = board_x * 3 + board_y

        if self.buttons[x][y].text() == '' and (
                self.main_board[board_x][board_y] is None or self.next_allowed_board is not None and
                self.main_board[board_x][board_y] is not None):
            self.buttons[x][y].setText(self.current_player)
            self.sub_boards[board_index][cell_x][cell_y] = self.current_player
            if self.checkWin(self.sub_boards[board_index]):
                self.main_board[board_x][board_y] = self.current_player
                self.replaceSubBoardWithBigSymbol(board_x, board_y)
                if self.checkWin(self.main_board):
                    QMessageBox.information(self, "Game Over", f"Player {self.left_nickname if self.current_player == 'X' else self.left_nickname} wins!")
                    self.resetGame()
                    return
            elif self.isBoardFull(self.sub_boards[board_index]):
                self.main_board[board_x][board_y] = "-"
                self.replaceSubBoardWithBigSymbol(board_x, board_y, is_tie=True)
            if self.checkGlobalDraw():
                QMessageBox.information(self, "Game Over", "It's a draw!")
                self.resetGame()
                return
            self.current_player = 'O' if self.current_player == 'X' else 'X'
            self.next_allowed_board = cell_x * 3 + cell_y
            if self.main_board[cell_x][cell_y] is not None:
                self.next_allowed_board = None
            self.highlightBoard()
            self.status_label.setText(f"Player {self.current_player}'s turn")
        else:
            QMessageBox.warning(self, "Invalid Move", "This cell is already occupied or the sub-board is finished!")

    def checkWin(self, board):
        for row in board:
            if row[0] == row[1] == row[2] and row[0] is not None:
                return True
        for col in zip(*board):
            if col[0] == col[1] == col[2] and col[0] is not None:
                return True
        if board[0][0] == board[1][1] == board[2][2] and board[0][0] is not None:
            return True
        if board[0][2] == board[1][1] == board[2][0] and board[0][2] is not None:
            return True
        return False

    def isBoardFull(self, board):
        for row in board:
            if None in row:
                return False
        return True

    def checkGlobalDraw(self):
        for row in self.main_board:
            for cell in row:
                if cell is None:
                    return False
        return True

    def highlightBoard(self):
        for i in range(9):
            for j in range(9):
                board_x, cell_x = divmod(i, 3)
                board_y, cell_y = divmod(j, 3)
                board_index = board_x * 3 + board_y
                if self.next_allowed_board is None or self.next_allowed_board == board_index:
                    if self.main_board[board_x][board_y] is None and self.buttons[i][j].text() == '':
                        self.buttons[i][j].setEnabled(True)
                        self.buttons[i][j].setStyleSheet("background-color: lightgrey")
                    else:
                        self.buttons[i][j].setEnabled(False)
                        self.buttons[i][j].setStyleSheet("")
                elif self.next_allowed_board is not None and self.main_board[board_x][board_y] is not None:
                    if self.buttons[i][j].text() == '':
                        self.buttons[i][j].setEnabled(True)
                        self.buttons[i][j].setStyleSheet("background-color: lightgrey")
                    else:
                        self.buttons[i][j].setEnabled(False)
                        self.buttons[i][j].setStyleSheet("")
                else:
                    self.buttons[i][j].setEnabled(False)
                    self.buttons[i][j].setStyleSheet("")

    def replaceSubBoardWithBigSymbol(self, board_x, board_y, is_tie=False):
        if is_tie:
            color = QColor("black")
            symbol = "-"
        else:
            color = self.X_color if self.current_player == 'X' else self.O_color
            symbol = self.current_player

        if self.main_board[board_x][board_y] == 'X':
            symbol = 'X'
            color = self.X_color
        elif self.main_board[board_x][board_y] == 'O':
            symbol = 'O'
            color = self.O_color
        elif self.main_board[board_x][board_y] == '-':
            symbol = '-'
            color = QColor("black")

        for i in range(3):
            for j in range(3):
                btn = self.buttons[board_x * 3 + i][board_y * 3 + j]
                btn.hide()

        sub_board_widget = self.mini_grid_widgets[board_x][board_y]
        sub_board_layout = sub_board_widget.layout()

        symbol_label = QLabel(symbol, self)
        symbol_label.setAlignment(Qt.AlignCenter)
        symbol_label.setFont(QFont("Arial", 100, QFont.Bold))
        symbol_label.setStyleSheet(f"color: {color.name()}")
        sub_board_layout.addWidget(symbol_label)
    def resetGame(self):
        self.current_player = 'X'
        self.main_board = [[None for _ in range(3)] for _ in range(3)]
        self.sub_boards = [[[None for _ in range(3)] for _ in range(3)] for _ in range(9)]
        self.next_allowed_board = None

        for i in range(9):
            for j in range(9):
                btn = self.buttons[i][j]
                btn.setText('')
                btn.setEnabled(False)
                btn.setStyleSheet("")
                btn.show()

        for i in range(3):
            for j in range(3):
                sub_board_widget = self.mini_grid_widgets[i][j]
                sub_board_layout = sub_board_widget.layout()
                for k in reversed(range(sub_board_layout.count())):
                    item = sub_board_layout.itemAt(k)
                    if isinstance(item.widget(), QLabel):
                        widget_to_remove = item.widget()
                        sub_board_layout.removeWidget(widget_to_remove)
                        widget_to_remove.deleteLater()


        self.status_label.setText("Press 'Start Game' to begin")
        self.x_color = QColor('blue')
        self.o_color = QColor('red')


        self.left_nickname_edit.setEnabled(True)
        self.right_nickname_edit.setEnabled(True)
        self.right_image_button.setEnabled(True)
        self.left_image_button.setEnabled(True)
        self.start_action.setEnabled(True)
        self.x_color_action.setEnabled(True)
        self.o_color_action.setEnabled(True)
        self.save_action.setEnabled(False)

    def saveGame(self):
        game_state = {
            'current_player': self.current_player,
            'main_board': self.main_board,
            'sub_boards': self.sub_boards,
            'next_allowed_board': self.next_allowed_board,
            'X_color': self.X_color.name(),
            'O_color': self.O_color.name(),
            'left_image_path': self.left_image_path,
            'right_image_path': self.right_image_path
        }
        file_name, _ = QFileDialog.getSaveFileName(self, "Save Game", "", "JSON Files (*.json)")
        if file_name:
            with open(file_name, 'w') as f:
                json.dump(game_state, f)
            QMessageBox.information(self, "Game Saved", "The game has been saved successfully!")

    def loadGame(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Load Game", "", "JSON Files (*.json)")
        if file_name:
            with open(file_name, 'r') as f:
                game_state = json.load(f)
            self.current_player = game_state['current_player']
            self.main_board = game_state['main_board']
            self.sub_boards = game_state['sub_boards']
            self.next_allowed_board = game_state['next_allowed_board']
            self.X_color = QColor(game_state['X_color'])
            self.O_color = QColor(game_state['O_color'])
            self.left_image_path = game_state.get('left_image_path', '')
            self.right_image_path = game_state.get('right_image_path', '')

            for i in range(9):
                for j in range(9):
                    board_x, cell_x = divmod(i, 3)
                    board_y, cell_y = divmod(j, 3)
                    board_index = board_x * 3 + board_y
                    if self.sub_boards[board_index][cell_x][cell_y] is not None:
                        self.buttons[i][j].setText(self.sub_boards[board_index][cell_x][cell_y])
                    else:
                        self.buttons[i][j].setText('')

            for i in range(3):
                for j in range(3):
                    if self.main_board[i][j] is not None:
                        self.replaceSubBoardWithBigSymbol(i, j, self.main_board[i][j] == "-")

            self.highlightBoard()
            self.status_label.setText(f"Game Loaded! Player {self.current_player}'s turn")

            if self.left_image_path:
                self.left_image_label.setPixmap(
                    QPixmap(self.left_image_path).scaled(self.left_image_label.size(), Qt.KeepAspectRatio))
            if self.right_image_path:
                self.right_image_label.setPixmap(
                    QPixmap(self.right_image_path).scaled(self.right_image_label.size(), Qt.KeepAspectRatio))

            self.left_nickname_edit.setEnabled(False)
            self.right_nickname_edit.setEnabled(False)
            self.right_image_button.setEnabled(False)
            self.left_image_button.setEnabled(False)
            self.start_action.setEnabled(False)
            self.x_color_action.setEnabled(False)
            self.o_color_action.setEnabled(False)
            self.save_action.setEnabled(True)
            QMessageBox.information(self, "Game Loaded", "The game has been loaded successfully!")


def main():
    app = QApplication(sys.argv)
    QApplication.setApplicationName("Ultimate Tic-Tac-Toe")
    QApplication.setWindowIcon(QIcon("icon.jpg"))
    ex = UltimateTicTacToe()
    ex.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
