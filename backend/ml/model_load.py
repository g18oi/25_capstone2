import pickle
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

MODEL_PATH = BASE_DIR / "model_rematch_probability.pkl"

MODEL_OBJECT = None

def load_prediction_model():
    global MODEL_OBJECT
    if MODEL_OBJECT is None:
        try:
            with open(MODEL_PATH, "rb") as f:
                MODEL_OBJECT = pickle.load(f)
            print(f"모델 로드 성공: {MODEL_PATH}")
        except FileNotFoundError:
            print(f"모델 파일 찾을 수 없음: {MODEL_PATH}")
        except Exception as e:
            print(f"모델 로드 중 오류 발생: {e}")

load_prediction_model()