# CoeiroClip
#
# COEIROINK 話者クラス
#
# Copyright (c) 2024-2026 led-mirage
# このソースコードは MITライセンス の下でライセンスされています。
# ライセンスの詳細については、このプロジェクトのLICENSEファイルを参照してください。

class CoeiroinkSpeaker:
    def __init__(self, speaker_uuid, style_id, name, style_name):
        # 話者UUID
        self.speaker_uuid = speaker_uuid
        # スタイルID
        self.style_id = style_id
        # キャラクター名    
        self.name = name
        # スタイル名
        self.style_name = style_name
