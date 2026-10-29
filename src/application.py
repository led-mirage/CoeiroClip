# CoeiroClip
#
# アプリケーションクラス
#
# Copyright (c) 2024-2026 led-mirage
# このソースコードは MITライセンス の下でライセンスされています。
# ライセンスの詳細については、このプロジェクトのLICENSEファイルを参照してください。

import argparse
import sys
from tkinter import messagebox

from app_logging import get_logger, setup_logging
from settings import Settings
from coeiroink import Coeiroink
from coeiroink_api import CoeiroinkAPI, CoeiroinkAPIError
from coeiroink_speaker import CoeiroinkSpeaker

APP_NAME = "CoeiroClip"
APP_VERSION = "0.3.0"
COPYRIGHT = "Copyright 2024-2026 led-mirage"

SETTING_FILE = "settings.json"

logger = get_logger("application")

class Application:
    # コンストラクタ
    def __init__(self):
        self.speakers: CoeiroinkSpeaker = None
        self.settings: Settings = None
        pass

    # 開始
    def start(self):
        parser = argparse.ArgumentParser(description=f"{APP_NAME} {APP_VERSION}")
        parser.add_argument("--setting", type=str, default=SETTING_FILE, help="設定ファイル名")
        args = parser.parse_args()

        self.print_apptitle()

        self.settings = Settings(args.setting)
        self.settings.load()

        CoeiroinkAPI.server = self.settings.get_coeiroink_server()
        Coeiroink.run_coeiroink(self.settings.get_coeiroink_install_path())

        try:
            speakers = CoeiroinkAPI.get_speakers()
        except CoeiroinkAPIError:
            logger.info(f"{APP_NAME} {APP_VERSION} stopped because COEIROINK is unavailable")
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
                result.append(CoeiroinkSpeaker(
                    speaker["speakerUuid"], style["styleId"],
                    speaker["speakerName"], style["styleName"]))
        return result

if __name__ == "__main__":
    log_file_path = setup_logging()

    if log_file_path is not None:
        logger.info(f"{APP_NAME} {APP_VERSION} started")

    try:
        from application import Application
        app = Application()
        app.start()
    except Exception as err:
        logger.exception("Application failed")

        message = (
            "An unexpected error occurred while the application was running.\n\n"
            f"{type(err).__name__}: {err}"
        )
        try:
            from ctypes import windll
            windll.user32.MessageBoxW(None, message, APP_NAME, 0x10)
        except Exception:
            pass

        raise SystemExit(1)
    else:
        logger.info(f"{APP_NAME} {APP_VERSION} stopped normally")
