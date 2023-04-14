# Uses model to predict bbox from image
from src.EldenRing.boss_detection.inference import BossDetectionReturn
# Get resized image dimensions for scaling purposes in the display
from src.EldenRing.boss_detection.config import RESIZE_WIDTH, RESIZE_HEIGHT
# Get path to images for testing purposes
from src.EldenRing.boss_detection.config import TRAIN_PATH
# Model retrieval
from src.EldenRing.boss_detection.config import OUT_DIR
# path definition and file retrieval
import os
# Handles imaging
import cv2
# yolo bbox translation for image display
from src.EldenRing.boss_detection.util import bbox_yolo_translation


# finds the corresponding bounding box Yolo file for a given image
def image2label_path(image_path, labels_path):
    image_filename = image_path.split("/")[-1]
    label_filename = image_filename.replace("png", "txt")
    return os.path.join(labels_path, label_filename).replace("\\", "/")


# This will handle image outputs for display
def pred_boxes(pred_img, pred_output):
    # output is a list
    outputs = pred_output[0]
    boxes = outputs['boxes']
    # define image size
    image_width = pred_img.shape[1]
    image_height = pred_img.shape[0]
    # resize the image
    image_scale_width = image_width / RESIZE_WIDTH
    image_scale_height = image_height / RESIZE_HEIGHT
    for i in range(len(boxes)):
        # grabs box dimensions and associated score
        box = [dim for dim in boxes[i]]
        score = outputs['scores'][i].item()
        # Limit length of score displayed
        score = str(score)[:5] if len(str(score)) > 5 else str(score)
        # Skips if no boss is found
        if len(box) < 1:
            continue
        # Grab bbox dimensions
        l = int(box[0] * image_scale_width)
        t = int(box[1] * image_scale_height)
        r = int(box[2] * image_scale_width)
        b = int(box[3] * image_scale_height)
        # BBox on image
        cv2.rectangle(pred_img, (l, t), (r, b), (0, 255, 0), 3)
        # Display confidence score
        cv2.putText(pred_img, str(score), (l, b), cv2.FONT_HERSHEY_SIMPLEX,
                    4.0, (0, 255, 0), 2, lineType=cv2.LINE_AA)
    return pred_img


# Adds true bounding box to image
def img_for_display(img_bbox_pair):
    # This will convert the image file to an image for display
    img_out = cv2.cvtColor(cv2.imread(img_bbox_pair[0], -1), cv2.COLOR_BGR2RGB)

    # Properly retrieve and format bounding box(es)
    with open(img_bbox_pair[1], 'r') as f:
        data = f.readlines()
    for dt in data:
        _, l, t, r, b = bbox_yolo_translation(dt, img_out.shape[0], img_out.shape[1])

    if len(data) > 0:
        # Imprints Bounding Box onto image
        # noinspection PyUnboundLocalVariable
        cv2.rectangle(img_out, (l, t), (r, b), (255, 0, 255), 3)
        return img_out
    elif len(data) == 0:
        return img_out
    else:
        raise RuntimeError


# Find root folder
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
TRAIN_PATH = os.path.join(project_root, TRAIN_PATH).replace("..", '')
OUT_DIR = os.path.join(project_root, OUT_DIR).replace("..", '')

# Define the path for needed components
TRAIN_IMAGES_PATH = os.path.join(TRAIN_PATH, 'images').replace("\\", "/")
TRAIN_LABELS_PATH = os.path.join(TRAIN_PATH, 'labels').replace("\\", "/")
MODEL_PATH = os.path.join(OUT_DIR, 'model100.pth').replace("\\", "/")

# Creates list of image paths
train_images = [f for f in os.listdir(TRAIN_IMAGES_PATH) if os.path.isfile(os.path.join(TRAIN_IMAGES_PATH, f))]
train_image_paths = [os.path.join(TRAIN_IMAGES_PATH, f).replace("\\", "/") for f in train_images]

# Model Retrieval
detection_model = BossDetectionReturn(MODEL_PATH)

# Grab image and labels
img1_path = train_image_paths[0]
img1_true = image2label_path(img1_path, TRAIN_LABELS_PATH)
img2_path = train_image_paths[205]
img2_true = image2label_path(img2_path, TRAIN_LABELS_PATH)
img3_path = train_image_paths[361]
img3_true = image2label_path(img3_path, TRAIN_LABELS_PATH)

# convert image_path to image
img1 = cv2.cvtColor(cv2.imread(img1_path, -1), cv2.COLOR_BGR2RGB)
img2 = cv2.cvtColor(cv2.imread(img2_path, -1), cv2.COLOR_BGR2RGB)
img3 = cv2.cvtColor(cv2.imread(img3_path, -1), cv2.COLOR_BGR2RGB)

# run image through the model
img1_resized, img1_pred = detection_model.boss_detection(img1)
img2_resized, img2_pred = detection_model.boss_detection(img2)
img3_resized, img3_pred = detection_model.boss_detection(img3)

# Returns the image with predicted bbox
pred1_img = pred_boxes(img1.copy(), img1_pred)
pred2_img = pred_boxes(img2.copy(), img2_pred)
pred3_img = pred_boxes(img3.copy(), img3_pred)

# Put bounding box on image
img1 = img_for_display((img1_path, img1_true))
img2 = img_for_display((img2_path, img2_true))
img3 = img_for_display((img3_path, img3_true))

# Place Images for display in a list
img_display = [img1, pred1_img, img2, pred2_img, img3, pred3_img]

# Display images for checking it
for img in img_display:
    cv2.imshow("image", cv2.resize(cv2.cvtColor(img, cv2.COLOR_RGB2BGR), (RESIZE_WIDTH, RESIZE_HEIGHT)))
    cv2.waitKey(0)
