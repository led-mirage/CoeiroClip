# CoeiroClip
#
# COEIROINK APIクラス
#
# Copyright (c) 2024-2026 led-mirage
# このソースコードは MITライセンス の下でライセンスされています。
# ライセンスの詳細については、このプロジェクトのLICENSEファイルを参照してください。

import requests


class CoeiroinkAPIError(Exception):
    """Raised when a COEIROINK API request or response processing fails."""


class CoeiroinkAPI:
    DEFAULT_SERVER = "http://127.0.0.1:50032"
    server = DEFAULT_SERVER

    # ステータスを取得する
    @staticmethod
    def get_status() -> str:
        try:
            response = requests.get(f"{CoeiroinkAPI.server}/")
            response.raise_for_status()
            status = response.json()["status"]
            if not isinstance(status, str):
                raise CoeiroinkAPIError("COEIROINK returned an invalid status")
            return status
        except CoeiroinkAPIError:
            raise
        except Exception as err:
            raise CoeiroinkAPIError("Failed to get COEIROINK status") from err

    # 話者リストを取得する
    @staticmethod
    def get_speakers() -> list[dict]:
        try:
            response = requests.get(f"{CoeiroinkAPI.server}/v1/speakers")
            response.raise_for_status()
            speakers = response.json()
            if not isinstance(speakers, list):
                raise CoeiroinkAPIError("COEIROINK returned an invalid speaker list")
            return speakers
        except CoeiroinkAPIError:
            raise
        except Exception as err:
            raise CoeiroinkAPIError("Failed to get COEIROINK speakers") from err

    # テキストの読み上げ用データを取得する
    @staticmethod
    def estimate_prosody(text: str) -> dict:
        try:
            post_params = {"text": text}
            response = requests.post(f"{CoeiroinkAPI.server}/v1/estimate_prosody", json=post_params)
            response.raise_for_status()
            prosody = response.json()
            if not isinstance(prosody, dict):
                raise CoeiroinkAPIError("COEIROINK returned invalid prosody data")
            return prosody
        except CoeiroinkAPIError:
            raise
        except Exception as err:
            raise CoeiroinkAPIError("Failed to estimate COEIROINK prosody") from err

    # 音声データを生成する
    @staticmethod
    def synthesis(speaker_uuid: str, style_id: int, text: str, prosody: dict,
                  speedScale = 1, volumeScale = 1, pitchScale = 0, intonationScale = 1,
                  prePhonemeLength = 0.1, postPhonemeLength = 0.1, outputSamplingRate = 24000) -> bytes:
        try:
            post_params = {
                "speakerUuid": speaker_uuid,
                "styleId": style_id,
                "text": text,
                "prosodyDetail": prosody["detail"],
                "speedScale": speedScale,
                "volumeScale": volumeScale,
                "pitchScale": pitchScale,
                "intonationScale": intonationScale,
                "prePhonemeLength": prePhonemeLength,
                "postPhonemeLength": postPhonemeLength,
                "outputSamplingRate": outputSamplingRate
            }
            response = requests.post(f"{CoeiroinkAPI.server}/v1/synthesis", json=post_params)
            try:
                response.raise_for_status()
            except requests.exceptions.HTTPError as err:
                response_detail = response.text.strip()
                if response_detail:
                    message = (
                        f"COEIROINK synthesis returned HTTP {response.status_code}: "
                        f"{response_detail}"
                    )
                else:
                    message = f"COEIROINK synthesis returned HTTP {response.status_code}"
                raise CoeiroinkAPIError(message) from err
            wave_data = response.content
            if not wave_data:
                raise CoeiroinkAPIError("COEIROINK returned empty audio data")
            return wave_data
        except CoeiroinkAPIError:
            raise
        except Exception as err:
            raise CoeiroinkAPIError("Failed to synthesize COEIROINK audio") from err

    # 音声データを生成する
    @staticmethod
    def get_wave_data(speaker_uuid: str, style_id: int, text: str,
                      speedScale = 1, volumeScale = 1, pitchScale = 0, intonationScale = 1,
                      prePhonemeLength = 0.1, postPhonemeLength = 0.1, outputSamplingRate = 24000) -> bytes:
        try:
            prosody = CoeiroinkAPI.estimate_prosody(text)

            return CoeiroinkAPI.synthesis(speaker_uuid, style_id, text, prosody,
                                          speedScale, volumeScale, pitchScale, intonationScale,
                                          prePhonemeLength, postPhonemeLength, outputSamplingRate)
        except CoeiroinkAPIError:
            raise
        except Exception as err:
            raise CoeiroinkAPIError("Failed to get COEIROINK audio data") from err
