import os
import numpy as np
from PIL import Image

from studiolab_ml.common import get_session, input_preprocess, package_root, verify_model
from studiolab_ml.mlft_utils import (
    get_class_list, seller_major_filer, neck_filter, 
    sleeve_filter, instance_heirarchy, get_nick_name,
    detection_preprocess, DetPostProcess,
    major_ins_keys, minor_ins_keys, attr_keys, 
    attr_dict, attr_keys_per_ins
)

# TODO: using cloud url with key


class MLFT:
    model_urls = {
        '1.0': {
            "detection": {
                "local": os.path.join(package_root, "models/mlft_det.onnx"),
                "url": "mlft/mlft_det_v1.0.onnx"
            },
            "classification": {
                "local": os.path.join(package_root, "models/mlft_cls.onnx"),
                "url": "mlft/mlft_cls_v1.0.onnx"
            }
        }
    }
    def __init__(
            self, 
            version: str = '1.0',
            use_gpu: bool = False,
            aws_access_key_id: str = None,
            aws_secret_access_key: str = None,
            detections_per_img: int = 100,
            nms_threshold: float = 0.5,
            min_score: float = 0.2,
        ): 
        det_path = self.model_urls[version]['detection']        
        det_path = verify_model(det_path, aws_access_key_id, aws_secret_access_key)        
        self.det =get_session(det_path, use_gpu)

        cls_path = self.model_urls[version]['classification']
        cls_path = verify_model(cls_path, aws_access_key_id, aws_secret_access_key)
        self.cls = get_session(cls_path, use_gpu)
        
        self.det_input_name = self.det.get_inputs()[0].name
        self.det_output_names = [output.name for output in self.det.get_outputs()]
        self.cls_input_name = self.cls.get_inputs()[0].name

        self.instance_list, self.det_key_list = get_class_list(
            major_ins_keys + minor_ins_keys, 
            return_keys=True
        )

        self.det_postprocess = DetPostProcess(detections_per_img, nms_threshold, min_score)
        print("Warming up...") #TODO: need logging?
        dummy_input = np.random.randn(1, 3, 224, 224).astype(np.float32)
        _ = self.cls.run(None, {self.cls_input_name: dummy_input})
        dummy_input = np.random.randn(1, 3, 640, 640).astype(np.float32)
        _ = self.det.run(None, {self.det_input_name: dummy_input})

    def predict(
            self, 
            image: Image.Image,
            target_category_id: int = None
        ):
        '''
        Predict MLFT result
        '''
        det_input, img_meta = detection_preprocess(image, 640)
        det_out = self.det.run(self.det_output_names, {self.det_input_name: det_input})
        det_out = self.det_postprocess(det_out, img_meta)
        xyxy = det_out[0]
        pred_cls = det_out[1]
        det_conf = det_out[2]

        # Filtering detection result by target category
        pred_cls = seller_major_filer(pred_cls, det_conf, xyxy, self.instance_list, target_category_id)
        
        pred_cls = neck_filter(pred_cls, det_conf, xyxy, self.instance_list)
        
        pred_id = 0
        results = []
        for xyxy_, p, c in zip(xyxy, pred_cls, det_conf):
            if p == -1: continue
            instance_name = self.instance_list[int(p)]
            ins_dict = {
                "id": pred_id,
                "bbox": xyxy_.tolist(),
                "supercategory": self.det_key_list[int(p)],
                "cls": instance_name,
                "conf": float(c),
                "attributes": {}
            }
            pred_id += 1
            x1, y1, x2, y2 = int(xyxy_[0]), int(xyxy_[1]), int(xyxy_[2]), int(xyxy_[3])
            cls_img = image.crop((x1, y1, x2, y2))
            cls_out = self.cls.run(None, {self.cls_input_name: input_preprocess(cls_img, 224)})
            attr_map = attr_keys_per_ins.get(self.det_key_list[int(p)], [])
            if len(attr_map) != 0:
                for k, attr_pred in zip(attr_keys, cls_out):
                    if k not in attr_map: continue
                    cls_idx = np.argmax(attr_pred)
                    if cls_idx == 0: continue
                    ins_dict["attributes"].update({k: attr_dict[k][cls_idx]})

            results.append(ins_dict)
        
        # Get heirarchy of instance
        results = instance_heirarchy(results)

        sleeve_filter(results)
        get_nick_name(results)
        return results