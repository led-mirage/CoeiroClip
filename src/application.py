# CoeiroClip
#
# アプリケーションクラス
#
# Copyright (c) 2024 led-mirage
# このソースコードは MITライセンス の下でライセンスされています。
# ライセンスの詳細については、このプロジェクトのLICENSEファイルを参照してください。

import sys
from tkinter import messagebox

from settings import Settings
from coeiroink import Coeiroink
from coeiroink_api import CoeiroinkAPI
from coeiroink_speaker import CoeiroinkSpeaker

APP_NAME = "CoeiroClip"
APP_VERSION = "0.2.2"
COPYRIGHT = "Copyright 2024 led-mirage"

SETTING_FILE = "settings.json"

class Application:
    # コンストラクタ
    def __init__(self):
        self.speakers: CoeiroinkSpeaker = None
        self.settings: Settings = None
        pass

    # 開始
    def start(self):
        self.print_apptitle()

        self.settings = Settings(SETTING_FILE)
        self.settings.load()

        CoeiroinkAPI.server = self.settings.get_coeiroink_server()
        Coeiroink.run_coeiroink(self.settings.get_coeiroink_install_path())

        speakers = CoeiroinkAPI.get_speakers()
        if speakers is None:
            message = "COEIROINK を起動してから使ってね"
            print(message)
            messagebox.showerror(f"{APP_NAME}", message)
            sys.exit()
        self.speakers = self.convert_speakers(speakers)

        from main_window import MainWindow
        main_window = MainWindow(self)
        main_window.show()
        main_window.terminate()
    
    # タイトルを表示する
    def print_apptitle(self):
        print(f"----------------------------------------------------------------------")
        print(f" {APP_NAME} {APP_VERSION}")
        print(f"")
        print(f" {COPYRIGHT}")
        print(f"----------------------------------------------------------------------")
        print(f"")

    # CoeiroinkAPIから帰ってきた話者リストをアプリケーションのモデルに変換する
    def convert_speakers(self, speakers):
        result = []
        for speaker in speakers:
            for style in speaker["styles"]:
                result.append(CoeiroinkSpeaker(style["styleId"], speaker["speakerName"], style["styleName"]))
        return result

if __name__ == "__main__":
    from application import Application
    app = Application()
    app.start()
