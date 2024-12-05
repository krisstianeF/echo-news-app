from PyQt5 import QtGui

def font(family, size):
    font = QtGui.QFont()
    font.setFamily(family)
    font.setPointSize(size)
    return font

class Style():
    white = "#ffffff"
    black = "#000000"

    blue110 = "#237DE3"
    blue100 = "#2C88F0"
    blue70 = "#6BB0FF"
    blue60 = "#9AC6F9"
    blue50 = "#B1D5FF"
    blue40 = "#C7E0FD"
    blue30 = "#E5F1FF"
    blue20 = "#F1F8FF"
    blue10 = "#F9FCFF"

    pink100 = "#FF56D0"

    error = "#F11843"

    scrollStyle = f'''QScrollArea {{ border: none;
                                        background-color: rgba(255, 255, 255, 0);}}
    
                    /* VERTICAL SCROLLBAR */
                     QScrollBar:vertical {{
                        border: none;
                        background: rgb(255, 255, 255);
                        width: 14px;
                        margin: 15px 0 15px 0;
                        border-radius: 0px;}}

                    /*  HANDLE BAR VERTICAL */
                    QScrollBar::handle:vertical {{	
                        background-color: rgb(154, 198, 249);
                        min-height: 30px;
                        border-radius: 7px;}}
                    QScrollBar::handle:vertical:hover{{	
                        background-color: rgb(177, 213, 255);}}
                    QScrollBar::handle:vertical:pressed {{	
                        background-color: rgb(177, 213, 255);}}

                    /* BTN TOP - SCROLLBAR */
                    QScrollBar::sub-line:vertical {{
                        border: none;
                        background-color: rgb(255, 255, 255);
                        height: 15px;
                        border-top-left-radius: 7px;
                        border-top-right-radius: 7px;
                        subcontrol-position: top;
                        subcontrol-origin: margin;}}
                    QScrollBar::sub-line:vertical:hover {{	
                        background-color: rgb(255, 255, 255);}}
                    QScrollBar::sub-line:vertical:pressed {{	
                        background-color: rgb(177, 213, 255);}}

                    /* BTN BOTTOM - SCROLLBAR */
                    QScrollBar::add-line:vertical {{
                        border: none;
                        background-color: rgb(255, 255, 255);
                        height: 15px;
                        border-bottom-left-radius: 7px;
                        border-bottom-right-radius: 7px;
                        subcontrol-position: bottom;
                        subcontrol-origin: margin;}}
                    QScrollBar::add-line:vertical:hover {{	
                        background-color: rgb(255, 255, 255);}}
                    QScrollBar::add-line:vertical:pressed {{	
                        background-color: rgb(177, 213, 255);}}

                    /* RESET ARROW */
                    QScrollBar::up-arrow:vertical, QScrollBar::down-arrow:vertical {{
                        background: none;}}
                    QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {{
                        background: none;}}'''

    lineEditStyle = f'''QLineEdit{{ 
        color: {black}; 
        background-color: {white}; 
        border: 1px solid {blue50}; 
        border-radius: 25px;
        padding-left: 20px;
        padding-right: 20px;}}'''
    lineEditStyleError = f'''
                            color: {black}; 
                            background-color: {white}; 
                            border: 1px solid {error}; 
                            border-radius: 25px;
                            padding-left: 20px;
                            padding-right: 20px;'''

    passwordFrameStyle = f'''
        QFrame{{ color: {black};   
        background-color: {white};   
        border: 1px solid {blue50};   
        border-radius: 25px;  
        padding-left: 10px;
        padding-right: 10px;}}'''
    passwordFrameStyleError = f'''
            QFrame{{ color: {black};   
            background-color: {white};   
            border: 1px solid {error};   
            border-radius: 25px;  
            padding-left: 10px;
            padding-right: 10px;}}'''

    @classmethod
    def change_to_dark_mode(cls):
        Style.white = "#000000"
        Style.black = "#ffffff"

    @classmethod
    def font(cls, family, size):
        font = QtGui.QFont()
        font.setFamily(family)
        font.setPointSize(size)
        return font