# CoeiroClip
#
# COEIROINK 制御用クラス
#
# Copyright (c) 2024-2026 led-mirage
# このソースコードは MITライセンス の下でライセンスされています。
# ライセンスの詳細については、このプロジェクトのLICENSEファイルを参照してください。

import os
import subprocess
import time

from coeiroink_api import CoeiroinkAPI, CoeiroinkAPIError

class Coeiroink:
    @staticmethod
    def run_coeiroink(coeiroink_path):
        if not Coeiroink.is_coeiroink_running():
            if os.path.isfile(coeiroink_path):
                subprocess.Popen(coeiroink_path, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                time.sleep(1)
                while not Coeiroink.is_coeiroink_running():
                    time.sleep(1)
                return True
            else:
                return False
        else:
            return True
    
    @staticmethod
    def is_coeiroink_running():
        try:
            CoeiroinkAPI.get_status()
            return True
        except CoeiroinkAPIError:
            return False
