from PyQt5 import QtGui

def font(family, size):
    font = QtGui.QFont()
    font.setFamily(family)
    font.setPointSize(size)
    return font

class Style():
    white = "#ffffff"
    black = "#090F15"

    blue110 = "#156FD5"
    blue100 = "#2C88F0"
    blue80 = "#4AAAFE"
    blue60 = "#7AC3FB"
    blue50 = "#9CD8FF"
    blue40 = "#C3EAFF"
    blue30 = "#D6F2FF"
    blue20 = "#E5F7FF"
    blue10 = "#F1FBFF"

    secondary110 = "#03D2E5"
    secondary100 = "#11EADC"
    secondary80 = "#3BF5D0"
    secondary60 = "#6AFADD"
    secondary40 = "#A2FFEC"
    secondary20 = "#C7FFF3"
    secondary10 = "#E9FFFA"

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