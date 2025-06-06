import torch
from transformers import (
    ViTForImageClassification,
    SwinForImageClassification,
    ConvNextForImageClassification,
)
from torchvision.models import densenet121, efficientnet_b0
import torch.nn as nn
from types import SimpleNamespace


class HuggingFaceStyleWrapper(nn.Module):
    def __init__(self, model):
        super().__init__()
        self.model = model

    def forward(self, x):
        logits = self.model(x)
        return SimpleNamespace(logits=logits)  # mimic HuggingFace output


def get_ViT_model():
    model = ViTForImageClassification.from_pretrained(
        "google/vit-base-patch16-224-in21k", num_labels=100
    )
    return model


def get_DenseNet_model():
    model = densenet121(pretrained=True)
    model.classifier = nn.Linear(model.classifier.in_features, 100)
    return HuggingFaceStyleWrapper(model)


def get_ConvNext_model():
    model = ConvNextForImageClassification.from_pretrained(
        # or 'convnext-small', 'convnext-tiny', etc.
        "facebook/convnext-base-224",
        num_labels=100,
        ignore_mismatched_sizes=True,
    )
    return model


def get_Swin_model():
    model = SwinForImageClassification.from_pretrained(
        "microsoft/swin-base-patch4-window7-224-in22k",
        num_labels=100,
        ignore_mismatched_sizes=True,
    )
    return model


def get_EfficientNet_model():
    model = efficientnet_b0(pretrained=True)  # Or b1, b2, ..., b7
    model.classifier[1] = nn.Linear(model.classifier[1].in_features, 100)
    return HuggingFaceStyleWrapper(model)


def get_model(model_name):
    model_name = model_name.lower()
    if model_name == "vit":
        return get_ViT_model()
    elif model_name == "swin":
        return get_Swin_model()
    elif model_name == "convnext":
        return get_ConvNext_model()
    elif model_name == "densenet":
        return get_DenseNet_model()
    elif model_name == "efficientnet":
        return get_EfficientNet_model()
    else:
        raise ValueError(f"Unknown model name: {model_name}")
