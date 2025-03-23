import os
os.environ['QT_QPA_PLATFORM'] = 'offscreen'  # Set platform to offscreen for web environment

import sys
from PyQt5.QtWidgets import QApplication
from gui import MainWindow

def main():
    try:
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        print(f"Error starting application: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()