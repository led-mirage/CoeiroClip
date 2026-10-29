# CoeiroClip
#
# アプリケーション設定クラス
#
# Copyright (c) 2024 led-mirage
# このソースコードは MITライセンス の下でライセンスされています。
# ライセンスの詳細については、このプロジェクトのLICENSEファイルを参照してください。

import json
import os
import threading

from coeiroink_api import CoeiroinkAPI

class Settings:
    FILE_VER = 3

    def __init__(self, setting_file_path):
        self._setting_file_path = setting_file_path
        self._lock = threading.Lock()
        self._init_member()

    def _init_member(self):
        self._speaker_uuid = ""
        self._speaker_style_id = 0
        self._speed_scale = 1.2
        self._pitch_scale = 0.0
        self._coeiroink_server = CoeiroinkAPI.DEFAULT_SERVER
        self._coeiroink_install_path = ""
        self._replacements = []

    # 話者UUIDとスタイルID
    def get_speaker(self):
        with self._lock:
            return self._speaker_uuid, self._speaker_style_id

    def set_speaker(self, speaker_uuid, speaker_style_id):
        with self._lock:
            self._speaker_uuid = speaker_uuid
            self._speaker_style_id = speaker_style_id

    def get_speaker_uuid(self):
        with self._lock:
            return self._speaker_uuid

    def get_speaker_style_id(self):
        with self._lock:
            return self._speaker_style_id

    # 読み上げスピード
    def get_speed_scale(self):
        with self._lock:
            return self._speed_scale

    def set_speed_scale(self, speed_scale):
        with self._lock:
            self._speed_scale = speed_scale

    # 声の高さ
    def get_pitch_scale(self):
        with self._lock:
            return self._pitch_scale

    def set_pitch_scale(self, pitch_scale):
        with self._lock:
            self._pitch_scale = pitch_scale

    # COEIROINK サーバーのURL
    def get_coeiroink_server(self):
        with self._lock:
            return self._coeiroink_server
    
    def set_coeiroink_server(self, coeiroink_server):
        with self._lock:
            self._coeiroink_server = coeiroink_server

    # COEIROINK のインストールパス
    def get_coeiroink_install_path(self):
        with self._lock:
            return self._coeiroink_install_path
    
    def set_coeiroink_install_path(self, install_path):
        with self._lock:
            self._coeiroink_install_path = install_path

    # 置換設定
    def get_replacements(self):
        with self._lock:
            return self._replacements
        
    def set_replacements(self, replacements):
        with self._lock:
            self._replacements = replacements

    # 設定ファイルを保存する
    def save(self):
        with self._lock:
            self._save_nolock()

    def _save_nolock(self):
        with open(self._setting_file_path, "w", encoding="utf-8") as file:
            setting = {}
            setting["file_ver"] = Settings.FILE_VER
            setting["speaker_uuid"] = self._speaker_uuid
            setting["speaker_style_id"] = self._speaker_style_id
            setting["speed_scale"] = self._speed_scale
            setting["pitch_scale"] = self._pitch_scale
            setting["coeiroink_server"] = self._coeiroink_server
            setting["coeiroink_install_path"] = self._coeiroink_install_path
            setting["replacements"] = self._replacements
            json.dump(setting, file, ensure_ascii=False, indent=4)

    # 設定ファイルを読み込む
    def load(self):
        if not os.path.exists(self._setting_file_path):
            self._init_member()
            self._save_nolock()
            return

        with self._lock:
            with open(self._setting_file_path, "r", encoding="utf-8") as file:
                setting = json.load(file)
                file_ver = setting.get("file_ver", 1)
                needs_migration = "speaker_style_id" not in setting and "speaker_id" in setting
                self._speaker_uuid = setting.get("speaker_uuid", self._speaker_uuid)
                self._speaker_style_id = setting.get(
                    "speaker_style_id", setting.get("speaker_id", self._speaker_style_id))
                self._speed_scale = setting.get("speed_scale", self._speed_scale)
                self._pitch_scale = setting.get("pitch_scale", self._pitch_scale)
                self._coeiroink_server = setting.get("coeiroink_server", self._coeiroink_server)
                self._coeiroink_install_path = setting.get("coeiroink_install_path", self._coeiroink_install_path)
                self._replacements = setting.get("replacements", self._replacements)

        if file_ver < Settings.FILE_VER or needs_migration:
            self._save_nolock()
