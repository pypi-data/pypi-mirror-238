from PIL import Image
from torchvision import transforms

IMAGE_NORMALIZATION_MEAN = [0.485, 0.456, 0.406]
IMAGE_NORMALIZATION_STD = [0.229, 0.224, 0.225]

LABELS = [
    "appendix",
    "ileocecal_valve",
    "polyp",
    "water_jet",
    "digital_chromo_endoscopy",
    "instrument",
    "wound",
    "blood",
    "ileum",
    "low_quality",
    "clip",
    "outside"
]

# Helper function to convert image to tensor
def image_to_tensor(image:Image.Image):
    transform = transforms.Compose([
        transforms.ToTensor(),
        transforms.Normalize(IMAGE_NORMALIZATION_MEAN, IMAGE_NORMALIZATION_STD)
    ])
    return transform(image)

def read_image(image_path, init_height=1080, target_height=512):
    # read image using cv2
    img = Image.open(image_path)
    img = resize_image(img, init_height, target_height)
    return img

def normalize_image(image:Image.Image):
    # normalize image
    normalized_image = transforms.Normalize(IMAGE_NORMALIZATION_MEAN, IMAGE_NORMALIZATION_STD)(image)
    return normalized_image

def resize_image(image:Image.Image, init_height=1080, target_height=512):
    # resize image to a height of 1080 while maintaining the aspect ratio
    resized_image = transforms.Resize(init_height)(image)
    
    # zeropad the image to a square
    width, height = resized_image.size
    max_dim = max(width, height)
    pad_width = (max_dim - width) // 2
    pad_height = (max_dim - height) // 2
    padding = (pad_width, pad_height, pad_width, pad_height)  # left, top, right, bottom
    resized_image = transforms.Pad(padding)(resized_image)

    # resize the image to 768x768
    resized_image = transforms.Resize(target_height)(resized_image)
    # ic(resized_image.size)

    return resized_image