import numpy as np
from .bbox import cxcyhw2xyxy, multiclass_nms

class DetPostProcess:
    def __init__(
        self,
        detections_per_img: int = 100,
        nms_threshold: float = 0.5,
        min_score: float = 0.2,
    ):
        self.image_size = [640, 640]
        self.detections_per_img = detections_per_img
        self.nms_thresh = nms_threshold
        self.min_score = min_score
        # self.single_img = True #TODO: will be updated later

    def __call__(
            self, 
            outputs: np.ndarray or list, #numpy array: single image, list: batch image
            meta: tuple or list #tuple : single image, list : batch image
        ):
        '''
        args:
            outputs(list or numpy array): [ np.array([bs, (x, y, w, h, obj, cls), num_instance]), ...]
            meta(list or tuple): [(ratio, (dw, dh), img_size), ...]
        '''
        outputs = np.squeeze(outputs[0]).T # dim = (num_instance, (x, y, w, h, obj, cls))

        # Filter out object confidence scores below threshold
        scores = outputs[:, 4:]
        predictions = np.argmax(scores, axis=1)
        scores = np.max(scores, axis=1)
        boxes = outputs[:, :4]
        predictions = predictions[scores > self.min_score]
        boxes = boxes[scores > self.min_score]
        scores = scores[scores > self.min_score]

        if len(scores) == 0:
            return np.array([]), np.array([]), np.array([])

        boxes = self.extract_boxes(boxes, meta)

        keep = multiclass_nms(boxes, scores, predictions, self.nms_thresh)

        scores = scores[keep]
        predictions = predictions[keep]
        boxes = boxes[keep]

        return boxes, predictions, scores
    
    def extract_boxes(self, boxes, meta):
        
        # Convert boxes to xyxy format
        boxes = cxcyhw2xyxy(boxes)

        # Scale boxes to original image dimensions
        boxes = self.rescale_boxes(boxes, meta)

        return boxes
    
    def rescale_boxes(self, boxes, meta):

        r_h, r_w = meta[0]
        pad_w, pad_h = meta[1]
        img_width, img_height = meta[2]
        boxes[:, 0::2] = (boxes[:, 0::2] - pad_w) / r_w
        boxes[:, 1::2] = (boxes[:, 1::2] - pad_h) / r_h
        return boxes
    
