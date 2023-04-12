import torch
import cv2
import numpy as np
import os

from torch.utils.data import Dataset, DataLoader

from util import retrieve_labels, bbox_yolo_translation, collate_fn
from config import CLASSES, TRAIN_PATH, VALIDATION_PATH, BATCH_SIZE, RESIZE_HEIGHT, RESIZE_WIDTH


class BossDetectionDataset(Dataset):
    def __init__(self, path, width, height, classes, transforms=None):
        self.image_path = os.path.join(path, 'images').replace("\\", "/")
        self.label_path = os.path.join(path, 'labels').replace("\\", "/")
        self.width = width
        self.height = height
        self.classes = classes
        self.transforms = transforms

        self.all_images = [f for f in os.listdir(self.image_path) if os.path.isfile(os.path.join(self.image_path, f))]

    def __getitem__(self, idx):
        # Retrieve image
        image_path = os.path.join(self.image_path, self.all_images[idx])
        image = cv2.imread(image_path)
        # Resize image to desired size
        image_resized = cv2.resize(image, (self.width, self.height))
        image_height = image_resized.shape[0]
        image_width = image_resized.shape[1]
        # Fix colors to torch standard
        image_resized = image_resized / 255.0

        # Capture all bboxes
        boxes = []
        labels = []
        annot_file_path = retrieve_labels(image_path, self.label_path)  # return path to bboxes
        with open(annot_file_path, 'r') as f:
            data = f.readlines()
        # translates bbox dimensions to desired format
        for dt in data:
            c, l, t, r, b = bbox_yolo_translation(dt, image_height, image_width)
            boxes.append([l, t, r, b])
            if c == 0:
                labels.append(1)
            elif c != 0:
                labels.append(0)
        # bounding box to tensor
        if len(boxes) > 0:
            boxes = torch.as_tensor(boxes, dtype=torch.float32)
        else:
            boxes = torch.zeros((0, 4))
        # area of the bounding boxes
        area = (boxes[:, 3] - boxes[:, 1]) * (boxes[:, 2] - boxes[:, 0])
        # no crowd instances
        iscrowd = torch.zeros((boxes.shape[0],), dtype=torch.int64)
        # labels to tensor
        labels = torch.as_tensor(labels, dtype=torch.int64)

        # prepare the final 'target' dictionary
        target = {}
        target["boxes"] = boxes
        target["labels"] = labels
        target["area"] = area
        target["iscrowd"] = iscrowd
        image_id = torch.tensor([idx])
        target["image_id"] = image_id

        # apply the image transforms
        if self.transforms:
            sample = self.transforms(image=image_resized,
                                     bboxes=target['boxes'],
                                     labels=labels)
            image_resized = sample['image']
            target['boxes'] = torch.Tensor(sample['bboxes'])

        # Final image formatting for pytorch model; pytorch requires (channel, height, width)
        out_image = torch.as_tensor(image_resized, dtype=torch.float32)
        out_image = out_image.permute(2, 0, 1)
        return out_image, target

    def __len__(self):
        return len(self.all_images)


# Prepare file path
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
TRAIN_PATH = os.path.join(project_root, TRAIN_PATH).replace("\\", "/").replace("..", "")
VALIDATION_PATH = os.path.join(project_root, VALIDATION_PATH).replace("\\", "/").replace("..", "")
# prepare the final datasets and data loaders
# if on a local Linux system, try using num_workers value 2 or more
train_dataset = BossDetectionDataset(TRAIN_PATH, RESIZE_WIDTH, RESIZE_HEIGHT, CLASSES, None)
valid_dataset = BossDetectionDataset(VALIDATION_PATH, RESIZE_WIDTH, RESIZE_HEIGHT, CLASSES, None)
train_loader = DataLoader(
    train_dataset,
    batch_size=BATCH_SIZE,
    shuffle=True,
    num_workers=0,
    collate_fn=collate_fn
)
valid_loader = DataLoader(
    valid_dataset,
    batch_size=BATCH_SIZE,
    shuffle=False,
    num_workers=0,
    collate_fn=collate_fn
)
print(f"Number of training samples: {len(train_dataset)}")
print(f"Number of validation samples: {len(valid_dataset)}\n")


# execute datasets.py using Python command from Terminal...
# ... to visualize sample images
# USAGE: python datasets.py
if __name__ == '__main__':
    # sanity check of the Dataset pipeline with sample visualization
    dataset = train_dataset
    print(f"Number of training images: {len(dataset)}")

    # function to visualize a single sample
    def visualize_sample(image, target):
        if len(target['boxes']) > 0:
            box = target['boxes'][0]
            label = CLASSES[target['labels']]
            cv2.rectangle(
                image,
                (int(box[0]), int(box[1])), (int(box[2]), int(box[3])),
                (0, 255, 0), 1
            )
            cv2.putText(
                image, label, (int(box[0]), int(box[1] - 5)),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2
            )
            cv2.imshow('Image', image)
            cv2.waitKey(0)


    NUM_SAMPLES_TO_VISUALIZE = 5
    for i in range(NUM_SAMPLES_TO_VISUALIZE):
        image, target = dataset[i]
        visualize_sample(image, target)
