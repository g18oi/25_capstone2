import re
import numpy as np
import torch
from PIL import Image
from transformers import AutoTokenizer, AutoModel 
import easyocr
import warnings
import fitz
import pickle
import os

warnings.filterwarnings('ignore')

class ChildcareDocumentClassifier:
    def __init__(self, similarity_threshold: float = 0.70):
        print("MPNet 모델 및 OCR 리더 로딩 중")
        self.mpnet_tokenizer = AutoTokenizer.from_pretrained("sentence-transformers/all-mpnet-base-v2")
        self.mpnet_model = AutoModel.from_pretrained("sentence-transformers/all-mpnet-base-v2")
        self.mpnet_model.eval()

        self.ocr_reader = easyocr.Reader(["ko", "en"], gpu=False)

        self.KEYWORDS = ["보육교사", "보육", "영유아보육법", "보육교사자격증", "유치원", "유아교육법", "교육법", "유아", "영유아"]
        self.REFERENCES = [
            "보육교사", "영유아보육법에 따라 보육교사의", "보육교사 1급", 
            "보육교사 2급", "보육교사 3급", "교원 자격증", "교육부장관"
        ]

        self.threshold = similarity_threshold
        print("모델 로딩 완료")

    def extract_text_mpnet_chandra(self, file_path: str) -> str:
        try:
            ext = os.path.splitext(file_path)[1].lower()

            if ext in ['.png', '.jpg', '.jpeg', '.tiff', '.bmp', '.webp']:
                image = Image.open(file_path).convert("RGB")
                result = self.easyocr_reader.readtext(np.array(image))
                text = " ".join([txt for _, txt, conf in result if conf > 0.3])
                return re.sub(r"\s+", " ", text).strip()
            
            elif ext == '.pdf':
                doc = fitz.open(file_path)

                text_chunks = []
                for page_num in range(min(3, len(doc))):
                    page = doc[page_num]
                    text = page.get_text()
                    if text.strip():
                        text_chunks.append(text)
                
                full_text = re.sub(r"\s+", " ", " ".join(text_chunks)).strip()

                if len(full_text) > 30:
                    doc.close()
                    return full_text
                
                ocr_chunks = []
                for page_num in range(min(3, len(doc))):
                    page = doc[page_num]
                    pix = page.get_pixmap(dpi=150)
                    img_data = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
                    
                    ocr_result = self.easyocr_reader.readtext(np.array(img_data))
                    page_ocr = " ".join([txt for _, txt, conf in ocr_result if conf > 0.3])
                    if page_ocr.strip():
                        ocr_chunks.append(page_ocr)
                
                ocr_text = re.sub(r"\s+", " ", " ".join(ocr_chunks)).strip()
                doc.close()
                print(f"PyMuPDF+EasyOCR: {len(ocr_text)}자")
                return ocr_text if ocr_text else os.path.splitext(os.path.basename(file_path))[0]
            
            else:
                print(f"미지원 형식: {ext}")
                return os.path.splitext(os.path.basename(file_path))[0]
        
        except Exception as e:
            print(f"처리 실패: {e}")
            return os.path.splitext(os.path.basename(file_path))[0]


    def mpnet_encode(self, sentences: list) -> torch.Tensor:
        if not sentences: return torch.empty((0, 768))
        encoded_input = self.mpnet_tokenizer(sentences, padding=True, truncation=True, max_length=384, return_tensors="pt")
        with torch.no_grad():
            model_output = self.mpnet_model(**encoded_input)
            embeddings = model_output.last_hidden_state[:, 0, :]
        return torch.nn.functional.normalize(embeddings, p=2, dim=1)

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
        if doc_embeddings.numel() == 0:
            return 0.0, 0
        similarities = torch.nn.functional.cosine_similarity(
            ref_embedding.unsqueeze(0),
            doc_embeddings,
            dim=1,
        )
        return float(similarities.max()), int(similarities.argmax())
    
    def classify_childcare_document(self, file_path: str, reference_sentences: list) -> dict:
        result = {
            "verdict": False, "max_confidence": 0.0, "matched_sentence": "",
            "total_sentences": 0, "raw_text": "", "reason": ""
        }

        raw_text = self.extract_text_mpnet_chandra(file_path)
        result["raw_text"] = raw_text

        doc_sentences = self.preprocess_sentences(raw_text)
        result["total_sentences"] = len(doc_sentences)

        if len(doc_sentences) == 0:
            result["reason"] = "문장 없음"
            return result

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
                    "score": score,
                    "matched_sentence": doc_sentences[doc_idx],
                }
            )

        max_match = max(best_matches, key=lambda x: x["score"])
        result["max_confidence"] = round(max_match["score"], 4)
        result["matched_sentence"] = max_match["matched_sentence"]
        result["verdict"] = max_match["score"] >= self.threshold

        return result

def classify_childcare_with_rules(self, file_path: str, base_threshold=0.70):
    result = self.classify_childcare_document(file_path, self.REFERENCES)
    score = result.get("max_confidence", 0.0)
    raw_text = result.get("raw_text", "")

    hit_count = sum(raw_text.count(kw) for kw in self.KEYWORDS)
    score += 0.02 * hit_count if hit_count > 0 else -0.05
        
    result["rule_score"] = round(score, 4)
    result["verdict"] = score >= base_threshold
    result["keyword_hit_count"] = hit_count
    return result

@classmethod
def load_model(cls, load_path: str):
    with open(load_path, 'rb') as f:
        return pickle.load(f)