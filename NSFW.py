from transformers import AutoFeatureExtractor, AutoModelForImageClassification
from PIL import Image
import torch
extractor = AutoFeatureExtractor.from_pretrained("Falconsai/nsfw_image_detection")
model = AutoModelForImageClassification.from_pretrained("Falconsai/nsfw_image_detection")
def nsfw_predict(img_path):
    image = Image.open(img_path).convert("RGB")
    inputs = extractor(images=image, return_tensors="pt")
    with torch.no_grad():
        outputs = model(**inputs)
        logits = outputs.logits
        probs = logits.softmax(dim=1)

    nsfw_score = float(probs[0][1])   
    sfw_score = float(probs[0][0])

    return nsfw_score*100

