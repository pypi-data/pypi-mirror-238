import os
import numpy as np
from PIL import Image

from studiolab_ml.common import get_session, input_preprocess, package_root, verify_model

# TODO: using cloud url with key



class PoseCompo:

    model_urls = {
        '1.0': {
            "local": os.path.join(package_root, "models/pcp.onnx"),
            "url": "pose_compo/pcp_beta.onnx" 
        }
    }

    pcp_meta = {
        "cut": ["outfit", "product", "detail", "noise"],
        "background": ['blind', 'outdoor', 'studio'],
        "direction": ["back", "front", "left", "left_45", "right", "right_45"],
        "head": ["head", "headless"],
        "part": ["bottom", "full", "top"],
        "pose": ["sit_in_chair", "sit_in_floor", "stand"],
        "detail":  ['bottom_hem', 'bottom_waist', 'button', 'fly', 'graphic_n_logo', 'hood', 'jacket_lining', 'lining', 'material', 'neck_back', 'neck_front', 'pocket', 'shoulder', 'sleeve', 'string', 'top_hem', 'top_waist', 'vent', 'zipper'],   
    }

    pcp_keys = ['cut', 'background', 'direction', 'head', 'part', 'pose', 'detail']

    def __init__(
            self, 
            version: str = '1.0',
            use_gpu: bool = False,
            aws_access_key_id: str = None,
            aws_secret_access_key: str = None,
        ): 
        path = self.model_urls[version]
        path = verify_model(path, aws_access_key_id, aws_secret_access_key)

        self.session = get_session(path, use_gpu)
        self.input_name = self.session.get_inputs()[0].name
        print("Warming up...") #TODO: logging?
        dummy_input = np.random.randn(1, 3, 224, 224).astype(np.float32)
        _ = self.session.run(None, {self.input_name: dummy_input})

    def predict(
            self,
            image: Image.Image
        ):
        image = input_preprocess(image, 224)
        outputs = self.session.run(None, {self.input_name: image})
        res = {pk: None for pk in self.pcp_keys}
        detail_probs = sigmoid(outputs[-1][0])
        outputs = outputs[:-1]
        for i, o in enumerate(outputs):
            outputs[i] = np.argmax(o[0], axis=-1)
        cut_pred = outputs[0]
        if self.pcp_meta['cut'][cut_pred] == 'noise':
            res['cut'] = 'noise'
        elif self.pcp_meta['cut'][cut_pred] == 'detail':
            detail_preds = (detail_probs > 0.5).astype(int)
            res['cut'] = 'detail'
            res['detail'] = []
            detail_cls = self.pcp_meta['detail']
            for i, p in enumerate(detail_preds):
                if p == 1:
                    res['detail'].append(detail_cls[i])
        elif self.pcp_meta['cut'][cut_pred] == 'outfit':
            res['cut'] = 'outfit'
            for i, pred in enumerate(outputs[1:]):
                res[self.pcp_keys[i+1]] = self.pcp_meta[self.pcp_keys[i+1]][pred]
        else:
            direction_pred = np.argmax(outputs[2], axis=-1)
            di_cls = self.pcp_meta['direction'][direction_pred]
            res['cut'] = 'product'
            res['direction'] = di_cls
        return res

def sigmoid(x):
    return 1 / (1 + np.exp(-x))