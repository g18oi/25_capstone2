from .ml.document import ChildcareDocumentClassifier

state = {} 

def get_verifier() -> ChildcareDocumentClassifier:
    if "verifier" not in state:
        raise RuntimeError("Document Verifier model not initialized.")
    return state["verifier"]