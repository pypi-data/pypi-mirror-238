def get_request_product_info(product_info: dict, nickname: str):
    """
    [제품 정보] 생성
    유저 입력 의류 정보와 닉네임을 포매팅
    """
    input_format = (
        "[제품 정보]\n"
        f"- 제품 이름: {product_info['title']}\n"
        f"- 제품 카테고리: {nickname}\n"
        f"- 제품 색상: {product_info['color_name']}\n"  # color_name 1개로 가정
        f"- 핏: {product_info['fit']}\n"
        f"- 계절감: {product_info['season']}\n"
        f"- 신축성: {product_info['elasticity']}\n"
        f"- 두께: {product_info['thickness']}\n"
        f"- 안감: {product_info['lining']}\n"
        f"- 비침: {product_info['through']}\n"
        f"- 촉감: {product_info['touch']}\n"
        f"- 재질: {product_info['material']}\n"
    )
    return input_format


def get_request_product_point(product_point: dict):
    """
    [제품 강조 포인트] 생성
    모든 mlft 결과의 key-value 쌍을 나열
    """
    input_format = "[제품 강조 포인트]\n"
    for key, value in product_point.items():
        if key == "nick_name":
            continue
        key_name = key.replace("_", " ")
        input_format += f"- {key_name}: {value}\n"
    return input_format
