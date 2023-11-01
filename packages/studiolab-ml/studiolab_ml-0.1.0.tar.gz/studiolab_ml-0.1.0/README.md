# STUDIOLAB ML inference Package

# Install
- pip install studiolab-ml
# RUN
All input image type is PIL Image 
## MLFT
 ```
from studiolab_ml import MLFT

mlft = MLFT()
out = mlft.predict(img, cat_id)
 ```
- result is same dict type as "get_attributes" in ML-API
## Pose Compo
```
from studiolab_ml import PoseCompo

pcp = PoseCompo()
out = pcp.predict(img)
```
- output examples
 - outfit image - {'cut': 'outfit', 'background': 'blind', 'direction': 'front', 'head': 'head', 'part': 'full', 'pose': 'stand', 'detail': None}
 - product image - {'cut': 'product', 'background': None, 'direction': 'front', 'head': None, 'part': None, 'pose': None, 'detail': None}
 - detail image - {'cut': 'detail', 'background': None, 'direction': None, 'head': None, 'part': None, 'pose': None, 'detail': [shoulder, sleeve, ..]}
 - noise image - {'cut': 'noise', 'background': None, 'direction': None, 'head': None, 'part': None, 'pose': None, 'detail': None}
# TODO
- create model cloud storage
- model download from cloud
- GPU inference