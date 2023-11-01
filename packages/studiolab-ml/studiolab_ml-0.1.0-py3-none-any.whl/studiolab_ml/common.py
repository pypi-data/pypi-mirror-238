import os
import numpy as np
from PIL import Image
import onnxruntime as ort

package_root = root_path = os.path.dirname(os.path.abspath(__file__))

mean=[0.485, 0.456, 0.406]
std=[0.229, 0.224, 0.225]

def get_session(
        model_path: str, 
        use_gpu: bool = False
    ):
    '''
    Get ONNX Runtime InferenceSession
    '''
    session = ort.InferenceSession(model_path)
    
    if use_gpu:
        providers = ['CUDAExecutionProvider']
        options = [{'device_id': '0'}]
        session.set_providers(providers, options)
    else:
        providers = ['CPUExecutionProvider']
        session.set_providers(providers)
    return session

def input_preprocess(
        image: Image.Image, 
        target_size: int
    ):
    '''
    Naive image resize and normalization
    '''
    if isinstance(image, Image.Image):
        pass
    else:
        raise TypeError('image must be PIL Image')
    # 이미지 크기 재조정
    image = image.resize((target_size, target_size))

    # 이미지를 numpy 배열로 변환
    img_array = np.array(image).astype(np.float32) / 255.0

    # 평균과 표준편차로 정규화
    img_array = (img_array - mean) / std

    # ONNX 입력 형식에 맞게 차원 변경 (NCHW format)
    img_array = img_array.transpose((2, 0, 1))
    img_array = np.expand_dims(img_array, axis=0)

    return img_array.astype(np.float32)


def verify_model(
        model_info: dict,
        aws_access_key_id: str,
        aws_secret_access_key: str,
        prompt: bool = False
    ):
    '''
    Check model info
    '''
    if prompt:
        model_path = model_info['prompt']['local']
    else:
        model_path = model_info['local']
        model_dir = os.path.dirname(model_path)
        os.makedirs(model_dir, exist_ok=True)
    if not os.path.exists(model_path):
        url = model_info.get('url', False)
        if url:
            model_download(
                aws_access_key_id,
                aws_secret_access_key,
                url,
                model_path
            )
        else:
            raise FileNotFoundError(f"{model_path} not found")
    return model_path
        

def model_download(
        aws_access_key_id: str, 
        aws_secret_access_key: str,
        source_path: str,
        target_path: str
    ):
    '''
    S3 authentication
    '''
    import boto3

    s3 = boto3.client(
        's3',
        region_name='ap-northeast-2',
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key
    )
    # meta = s3.head_object(Bucket=bucket_name, Key=key)
    bucket_name = 'sellercanvas-ml-model'
    key = source_path
    with open(target_path, 'wb') as f:
        s3.download_fileobj(bucket_name, key, f)
    f.close()