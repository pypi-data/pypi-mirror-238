from PIL import Image, ImageOps
import numpy as np

def cxcyhw2xyxy(x):
    # Convert bounding box (x, y, w, h) to bounding box (x1, y1, x2, y2)
    y = np.copy(x)
    y[..., 0] = x[..., 0] - x[..., 2] / 2
    y[..., 1] = x[..., 1] - x[..., 3] / 2
    y[..., 2] = x[..., 0] + x[..., 2] / 2
    y[..., 3] = x[..., 1] + x[..., 3] / 2
    return y

def compute_iou(box, boxes):
    # Compute xmin, ymin, xmax, ymax for both boxes
    xmin = np.maximum(box[0], boxes[:, 0])
    ymin = np.maximum(box[1], boxes[:, 1])
    xmax = np.minimum(box[2], boxes[:, 2])
    ymax = np.minimum(box[3], boxes[:, 3])

    # Compute intersection area
    intersection_area = np.maximum(0, xmax - xmin) * np.maximum(0, ymax - ymin)

    # Compute union area
    box_area = (box[2] - box[0]) * (box[3] - box[1])
    boxes_area = (boxes[:, 2] - boxes[:, 0]) * (boxes[:, 3] - boxes[:, 1])
    union_area = box_area + boxes_area - intersection_area

    # Compute IoU
    iou = intersection_area / union_area

    return iou

def bbox_inter(A, B):
    len_A = A.shape[0] #xyxy
    len_B = B.shape[0] #xyxy
    inter_ratio = np.zeros((len_A, len_B))
    
    for i in range(len_A):
        for j in range(len_B):
            xA = max(A[i, 0], B[j, 0])
            yA = max(A[i, 1], B[j, 1])
            xB = min(A[i, 2], B[j, 2])
            yB = min(A[i, 3], B[j, 3])
            
            intersection_area = max(0, xB - xA) * max(0, yB - yA)

            B_area = (B[j, 2] - B[j, 0]) * (B[j, 3] - B[j, 1])
            
            inter_ratio[i,j] = intersection_area /  B_area
            
    return inter_ratio

def nms(boxes, scores, iou_threshold, return_bool=False):
    """
    :param boxes: numpy array of bounding boxes in (x1, y1, x2, y2) format.
    :param scores: numpy array of scores associated with each box.
    :param iou_threshold: threshold for the IoU value to determine when a box should be suppressed.
    :return: list of indices of the boxes that survived NMS.
    """

    # Sort by score
    sorted_indices = np.argsort(scores)[::-1]

    keep_boxes = []
    while sorted_indices.size > 0:
        # Pick the last box
        box_id = sorted_indices[0]
        keep_boxes.append(box_id)

        # Compute IoU of the picked box with the rest
        ious = compute_iou(boxes[box_id, :], boxes[sorted_indices[1:], :])

        # Remove boxes with IoU over the threshold
        keep_indices = np.where(ious < iou_threshold)[0]

        # print(keep_indices.shape, sorted_indices.shape)
        sorted_indices = sorted_indices[keep_indices + 1]
    if return_bool:
        tmp = np.zeros_like(scores, dtype=bool)
        tmp[keep_boxes] = True
        return tmp
    return keep_boxes

def multiclass_nms(boxes, scores, class_ids, iou_threshold):

    unique_class_ids = np.unique(class_ids)

    keep_boxes = []
    for class_id in unique_class_ids:
        class_indices = np.where(class_ids == class_id)[0]
        class_boxes = boxes[class_indices,:]
        class_scores = scores[class_indices]

        class_keep_boxes = nms(class_boxes, class_scores, iou_threshold)
        keep_boxes.extend(class_indices[class_keep_boxes])

    return keep_boxes


def letterbox(
        image: Image.Image,
        new_shape: tuple= (640, 640),
        color:tuple = (114, 114, 114),
        auto: bool = False,
        scaleFill: bool = False,
        scaleup: bool = False,
        stride: int = 32,
    ):
    shape = image.size  # current shape [width, height]

    if isinstance(new_shape, int):
        new_shape = (new_shape, new_shape)

    # Scale ratio (new / old)
    r = min(new_shape[0] / shape[1], new_shape[1] / shape[0])
    if not scaleup:  # only scale down, do not scale up (for better val mAP)
        r = min(r, 1.0)

    # Compute padding
    ratio = r, r  # width, height ratios
    new_unpad = int(round(shape[0] * r)), int(round(shape[1] * r))
    dw, dh = (
        new_shape[1] - new_unpad[0],
        new_shape[0] - new_unpad[1],
    )  # wh padding
    if auto:  # minimum rectangle
        dw, dh = np.mod(dw, stride), np.mod(dh, stride)  # wh padding
    elif scaleFill:  # stretch
        dw, dh = 0.0, 0.0
        new_unpad = (new_shape[1], new_shape[0])
        ratio = (
            new_shape[1] / shape[1],
            new_shape[0] / shape[0],
        )  # width, height ratios

    dw /= 2  # divide padding into 2 sides
    dh /= 2

    # Resize
    if shape != new_unpad:
        image = image.resize(new_unpad, Image.BILINEAR)

    # Padding
    padding = (int(round(dw - 0.1)), int(round(dh - 0.1)), int(round(dw + 0.1)), int(round(dh + 0.1)))
    image = ImageOps.expand(image, padding, fill=color)

    return image, ratio, (dw, dh), shape