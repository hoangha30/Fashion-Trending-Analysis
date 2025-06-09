from torchvision.io import read_image
from torchvision.models.detection import MaskRCNN_ResNet50_FPN_Weights
from huggingface_hub import hf_hub_download
import onnxruntime

path_onnx = hf_hub_download(
    repo_id="rizavelioglu/fashionfail",
    filename="facere_base.onnx",  # or "facere_base.onnx"
)

# Load pre-trained model transformations.
weights = MaskRCNN_ResNet50_FPN_Weights.DEFAULT
transforms = weights.transforms()

# Load image and apply original transformation to the image.
img = read_image(r"C:\Users\hanhb\Documents\Trending-Fashion-Analysis\insta_img\1934742265222343043\1.jpg")
img_transformed = transforms(img)

# Create an inference session.
ort_session = onnxruntime.InferenceSession(
    path_onnx, providers=["CPUExecutionProvider"]
)

# Run inference on the input.
ort_inputs = {
    ort_session.get_inputs()[0].name: img_transformed.unsqueeze(dim=0).numpy()
}
ort_outs = ort_session.run(None, ort_inputs)

# Parse the model output.
boxes, labels, scores, masks = ort_outs

print("Label indices:", labels)
print("scores:", scores)