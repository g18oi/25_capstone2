import re
import numpy as np
import torch
from PIL import Image
from transformers import AutoTokenizer, AutoModel 
import easyocr
import warnings
import os

warnings.filterwarnings('ignore')

KEYWORDS = ["보육교사", "보육", "영유아보육법", "보육교사자격증", "유치원", "유아교육법", "교육법", "유아", "영유아"]

REFERENCES = [
    "보육교사",
    "영유아보육법에 따라 보육교사의",
    "보육교사 1급",
    "보육교사 2급",
    "보육교사 3급",
    "교원 자격증",
    "교육부장관",
]

class ChildcareDocumentClassifier:
    def __init__(self, similarity_threshold: float = 0.70):
        print("MPNet 모델 및 OCR 리더 로딩 중")

        self.mpnet_tokenizer = AutoTokenizer.from_pretrained("sentence-transformers/all-mpnet-base-v2")
        self.mpnet_model = AutoModel.from_pretrained("sentence-transformers/all-mpnet-base-v2")
        self.mpnet_model.eval()

        self.ocr_reader = easyocr.Reader(["ko", "en"], gpu=False)
        self.threshold = similarity_threshold
        
        print("모델 로딩 완료")

    def extract_text_mpnet_chandra(self, image_path: str) -> str:
        image = Image.open(image_path).convert("RGB")
        result = self.ocr_reader.readtext(np.array(image))
        text = " ".join([txt for _, txt, conf in result if conf > 0.3])
        return text.strip()

    def mpnet_encode(self, sentences: list) -> torch.Tensor:
        encoded_input = self.mpnet_tokenizer(
            sentences,
            padding=True,
            truncation=True,
            max_length=384,
            return_tensors="pt",
    )
        with torch.no_grad():
            model_output = self.mpnet_model(**encoded_input)
            embeddings = model_output.last_hidden_state[:, 0, :]
        embeddings = torch.nn.functional.normalize(embeddings, p=2, dim=1)
        return embeddings

    def preprocess_sentences(self, text: str) -> list:
        text = re.sub(r"[^\w\s가-힣\.!?0-9]", " ", text)            
        text = re.sub(r"\s+", " ", text).strip()
        text = re.sub(r"(습니다\.|입니다\.|다\.|요\.)", r"\1<SPLIT>", text)
        text = re.sub(r"([\.!?])", r"\1<SPLIT>", text)
        sentences = text.split("<SPLIT>")
        return [s.strip() for s in sentences if len(s.strip()) > 5]

    def compute_mpnet_similarity(
        self, ref_embedding: torch.Tensor, doc_embeddings: torch.Tensor
    ) -> tuple:
        similarities = torch.nn.functional.cosine_similarity(
            ref_embedding.unsqueeze(0),
            doc_embeddings,
            dim=1,
        )
        max_idx = similarities.argmax()
        return float(similarities[max_idx]), max_idx

    def classify_childcare_document(self, image_path: str, reference_sentences: list) -> dict:
        raw_text = self.extract_text_mpnet_chandra(image_path)
        doc_sentences = self.preprocess_sentences(raw_text)

        if len(doc_sentences) == 0:
            return {"verdict": False, "reason": "텍스트 추출 실패"}

        all_sentences = reference_sentences + doc_sentences
        all_embeddings = self.mpnet_encode(all_sentences)

        ref_embeddings = all_embeddings[: len(reference_sentences)]
        doc_embeddings = all_embeddings[len(reference_sentences) :]

        best_matches = []
        for i, ref_emb in enumerate(ref_embeddings):
            score, doc_idx = self.compute_mpnet_similarity(ref_emb, doc_embeddings)
            best_matches.append(
                {
                    "ref_idx": i,
                    "score": float(score),
                    "matched_sentence": doc_sentences[doc_idx],
                }
            )

        max_match = max(best_matches, key=lambda x: x["score"])
        verdict = max_match["score"] >= self.threshold

        return {
            "verdict": verdict,
            "max_confidence": round(max_match["score"], 4),
            "best_ref_idx": max_match["ref_idx"],
            "matched_sentence": max_match["matched_sentence"],
            "raw_text": raw_text,
        }

def classify_childcare_with_rules(
    classifier: ChildcareDocumentClassifier,
    image_path: str,
    references: list,
    base_threshold: float = 0.70,
    boost_per_hit: float = 0.02,
    penalty: float = 0.05,
) -> dict:
    result = classifier.classify_childcare_document(image_path, references)

    score = result["max_confidence"]

    raw_text = result.get("raw_text", "")

    hit_count = sum(raw_text.count(kw) for kw in KEYWORDS)

    if hit_count > 0:
        score = min(1.0, score + boost_per_hit * hit_count) 
        score -= penalty
        score = max(0.0, score)

    verdict = score >= base_threshold

    result["rule_score"] = round(score, 4)
    result["verdict"] = verdict
    result["keyword_hit_count"] = hit_count

    return result