import os
from dataclasses import dataclass
from typing import Union

import numpy as np
import supervision as sv
import torch
import open_clip
from autodistill.classification import ClassificationBaseModel
from autodistill.core.embedding_model import EmbeddingModel
from autodistill.core.embedding_ontology import EmbeddingOntology, compare_embeddings
from autodistill.detection import CaptionOntology
from autodistill.helpers import load_image

DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")


@dataclass
class FashionSigLIP(ClassificationBaseModel, EmbeddingModel):
    ontology: Union[EmbeddingOntology, CaptionOntology]

    def __init__(self, ontology: Union[EmbeddingOntology, CaptionOntology]):
        self.ontology = ontology

        self.model, _, self.preprocess = open_clip.create_model_and_transforms(
            'hf-hub:Marqo/marqo-fashionSigLIP', device=DEVICE
        )
        self.tokenizer = open_clip.get_tokenizer('hf-hub:Marqo/marqo-fashionSigLIP')
        self.model.eval().to(DEVICE)

        if isinstance(self.ontology, EmbeddingOntology):
            self.ontology.process(self)

        self.ontology_type = self.ontology.__class__.__name__

    def embed_image(self, input: str) -> np.ndarray:
        image = load_image(input, return_format="PIL")
        image = self.preprocess(image).unsqueeze(0).to(DEVICE)
        with torch.no_grad(), torch.amp.autocast(device_type="cuda"):
            features = self.model.encode_image(image)
            features /= features.norm(dim=-1, keepdim=True)
        return features.cpu().numpy()

    def embed_text(self, input: str) -> np.ndarray:
        tokens = self.tokenizer([input]).to(DEVICE)
        with torch.no_grad(), torch.amp.autocast(device_type="cuda"):
            features = self.model.encode_text(tokens)
            features /= features.norm(dim=-1, keepdim=True)
        return features.cpu().numpy()

    def predict(self, input: str) -> sv.Classifications:
        image = load_image(input, return_format="PIL")
        image_tensor = self.preprocess(image).unsqueeze(0).to(DEVICE)

        with torch.no_grad(), torch.amp.autocast(device_type="cuda"):
            image_features = self.model.encode_image(image_tensor)
            image_features /= image_features.norm(dim=-1, keepdim=True)

            if isinstance(self.ontology, EmbeddingOntology):
                return compare_embeddings(
                    image_features.cpu().numpy(),
                    self.ontology.embeddingMap.values()
                )
            else:
                labels = self.ontology.prompts()
                text_tokens = self.tokenizer(labels).to(DEVICE)
                text_features = self.model.encode_text(text_tokens)
                text_features /= text_features.norm(dim=-1, keepdim=True)

                probs = (image_features @ text_features.T).softmax(dim=-1).cpu().numpy()

                return sv.Classifications(
                    class_id=np.arange(len(labels)),
                    confidence=probs.flatten()
                )
