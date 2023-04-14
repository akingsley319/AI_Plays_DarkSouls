import torch


TRAIN_PATH = "../resources/EldenRing/BossImages/margityolo/train"
VALIDATION_PATH = "../resources/EldenRing/BossImages/margityolo/valid"

BATCH_SIZE = 4 # increase / decrease according to GPU memory
RESIZE_HEIGHT = 270 # resize the image for training and transforms
RESIZE_WIDTH = 480
NUM_EPOCHS = 100 # number of epochs to train for

DEVICE = torch.device("cuda") if torch.cuda.is_available else torch.device("cpu")

# classes: 0 index is reserved for background
# PyTorch Faster RCNN expects the background class
CLASSES = [
    'background', 'boss'
]
NUM_CLASSES = len(CLASSES)

# whether to visualize images after clearing the data loaders
VISUALIZE_TRANSFORMED_IMAGES = False

# location to save model and plots
OUT_DIR = "..resources/EldenRing/BossImages/margityolo/outputs"
SAVE_PLOTS_EPOCH = 2 # save loss plots after these many epochs
SAVE_MODEL_EPOCH = 2 # save model after these many epochs