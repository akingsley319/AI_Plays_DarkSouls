import torch
import cv2

from src.EldenRing.boss_detection.model import create_model
from src.EldenRing.boss_detection.config import RESIZE_WIDTH, RESIZE_HEIGHT, NUM_CLASSES


class BossDetectionReturn:
    def __init__(self, model_path, detection_threshold=0.8):
        # Determines the minimum confidence interval; if below this value, the bbox will be discarded
        self.detection_threshold = detection_threshold
        # Selects the device to be used
        self.device = torch.device('cuda') if torch.cuda.is_available() else torch.device('cpu')
        # load the model and the trained weights
        self.model = create_model(num_classes=NUM_CLASSES).to(self.device)
        self.model.load_state_dict(torch.load(
            model_path, map_location=self.device
        ))
        self.model.eval()

    def boss_detection(self, image):
        # Resize image to desired size
        image_resized = cv2.resize(image.copy(), (RESIZE_WIDTH, RESIZE_HEIGHT))
        # make the pixel range between 0 and 1
        image_resized = image_resized / 255.0
        # convert to tensor
        image_resized = torch.tensor(image_resized, dtype=torch.float32).cuda()
        # bring color channels to front
        image_resized = image_resized.permute(2, 0, 1)
        # add batch dimension
        image_resized = torch.unsqueeze(image_resized, 0)
        with torch.no_grad():
            outputs = self.model(image_resized)

        # load all detection to CPU for further operations
        outputs = [{k: v.to('cpu') for k, v in t.items()} for t in outputs]
        return image_resized, outputs
        # carry further only if there are detected boxes
        """
        if len(outputs[0]['boxes']) > 0:
            boxes = outputs[0]['boxes'].data.numpy()
            scores = outputs[0]['scores'].data.numpy()
            # filter out boxes according to `detection_threshold`
            boxes = boxes[scores >= self.detection_threshold]
            return boxes, scores
        else:
            return None, None
        """

