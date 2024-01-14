# CoeiroClip
#
# COEIROINK 話者クラス
#
# Copyright (c) 2024 led-mirage
# このソースコードは MITライセンス の下でライセンスされています。
# ライセンスの詳細については、このプロジェクトのLICENSEファイルを参照してください。

class CoeiroinkSpeaker:
    def __init__(self, id, name, style_name):
        # 話者ID
        self.id = id
        # キャラクター名    
        self.name = name
        # スタイル名
        self.style_name = style_name
