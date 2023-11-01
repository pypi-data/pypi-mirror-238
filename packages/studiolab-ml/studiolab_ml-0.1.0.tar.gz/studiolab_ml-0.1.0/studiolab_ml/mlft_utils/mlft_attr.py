import pandas as pd

#Update: 2023.09.01
deprecated = ["unisex", "floor", "not identified", "tutu", "innerwear"]

attr_dict = {
    "outer": [
        "None",
        "jacket",
        "coat",
        "cardigan"
    ],
    "skirt": [
        "None",
        "skirt"
    ],
    "pants": [
        "None",
        "pants",
        "jeans",
        "leggings"
    ],
    "dress": [
        "None",
        "dress",
        "jump suit"
    ],
    "top length": [
        "None",
        "under the knee",
        "above the hip",
        "hip",
        "knee",
        "cropped",
        # "not identified"
    ],
    "bottom length": [
        "None",
        "3/4",
        "cropped pants",
        "mini",
        "maxi",
        "half",
        # "floor",
        # "not identified"
    ],
    "fastening": [
        "None",
        "button",
        "string",
        "belt",
        "wrap & knot",
        "zipper",
        "buckle",
        "toggle"
    ],
    "breasted": [ # Moved from fastening
        "None",
        "single breasted",
        "double breasted"
    ],
    "pattern": [
        "None",
        "floral",        
        "plain",
        "check",
        "geometric & abstract",
        "stripe",
        "dot",
        "camouflage"
    ],
    "sleeve length": [
        "None",
        "long",
        "short sleeve",
        "not identified",
        "elbow",
        "sleeveless",
        "three quarter"
    ],
    "collar": [
        "None",
        "stand collar",
        "regular collar",
        "polo",
        "oversized collar",
        "notched collar",
        "no collar"
    ],
    "neckline": [
        "None",
        "spaghetti strap",
        "v-neck",
        "round",
        "square",
        "high-neck",
        "boat",
        "off shoulder"
    ],
    "hood": [
        "None",
        "hooded"
    ],
    "skirtline": [
        "None",
        "A-line",        
        "H-line",
        "wrap",
        "fit & flare",
        "pleated",
        "pencil",
        "tierd",
        "mermaid",
        # "tutu",
        # "not identified"
    ],
    "pantsline": [
        "None",
        "straight",
        "wide leg",
        "jogger",
        "slim",
        "skinny",
        "flared / boot",
        # "floor",
        # "not identified"
    ],
    "fit": [
        "None",
        "slim",
        "regular",
        "loosed",
        "oversized",
        "tight",
        # "not identified"
    ],
    "waist": [
        "None",
        "high waist",
        "normal waist",
        "low waist"
    ],
    "detail": [
        "None",
        "slit",
        "shirring",
        "logo",
        "ribbon",
        "lace",        
        "text", # Moved from pattern
        "picture", # Moved from pattern
    ],
    "pocket": [
        "None",
        "flap pocket",
        "normal pocket",
        "cargo pocket"
    ],
    "material": [
        "None",
        "knit",
        "denim",
        "fur",
        "wool",
        "leather",
        "corduroy",
        "mesh",
        "padded",
        "ribbed",
        "tweed",
        "suede",
        "rubber"
    ],
    "tpo": [
        "None",
        "party",
        "casual",
        "formal",
        "sport",
        "home & lounge"
    ],
    "style": [
        "None",
        "set-up",
        "suit",
        # "innerwear"
    ],
    "age": [
        "None",
        "adult",
        "child"
    ],
    "gender": [
        "None",
        "female",
        "male",
        # "unisex"
    ],
    "sub closet type": [
        "None",
        "slacks",
        "sweat pants",
        "sweat shirt",
        "windstopper"
    ],
    "top": [
        "None",
        "t-shirt",
        "blouse",
        "top",
        "shirt",
        "vest"
    ]
}
major_ins_keys = ["outer", "skirt", "pants", "dress", "top"]
minor_ins_keys = [
    'neckline', 'fastening', 'pocket', 'detail', 
    'collar', 'hood', 'sleeve length' 
]
attr_keys = ['tpo', 'gender', 'pantsline','waist',
             'bottom length', 'top length', 'skirtline', 'age',
             'material', 'pattern', 'style', 'fit', 'sub closet type',
             'breasted',
]

nc_lists = [len(attr_dict[k]) for k in attr_keys ]

attr_keys_per_ins = {
    "outer": ['top length', 'material', 'pattern', 'style', 'sub closet type', 'tpo', 'gender', 'age', 'fit'],
    "top": ['top length', 'material', 'pattern', 'style', 'sub closet type', 'tpo', 'gender', 'age', 'fit'],
    "skirt": ['bottom length', 'skirtline', 'waist', 'material', 'pattern', 'style', 'sub closet type', 'tpo', 'gender', 'age', 'fit'],
    "pants": ['bottom length', 'pantsline', 'waist', 'material', 'pattern', 'style', 'sub closet type', 'tpo', 'gender', 'age', 'fit'],
    "dress": ['top length', 'breasted', 'material', 'skirtline', 'pantsline', 'pattern', 'style', 'sub closet type', 'tpo', 'gender', 'age', 'fit'],
    'sleeve length': ['material', 'pattern'],
    'collar': ['material', 'pattern']
}

classes_of_seller_category = {
    0: ["jacket", "coat", "cardigan"],
    1: ["t-shirt", "blouse", "top", "shirt", "vest"],
    2: ["pants", "jeans", "leggings"],
    3: ["skirt"],
    4: ["dress"],
    5: ["vest"],
    6: ["jump suit"],
    # 7: [], #TODO 셋업
}

attr_dict_kr = {
    '아우터': [
        '없음', 
        '재킷', 
        '코트', 
        '가디건'
    ], 
    '상의': [
        '없음', 
        '티셔츠', 
        '블라우스', 
        '탑', 
        '셔츠', 
        '베스트'
    ], 
    '스커트': [
        '없음', 
        '스커트'
    ], 
    '바지': [
        '없음', 
        '팬츠', 
        '청바지', 
        '레깅스'
    ], 
    '원피스': [
        '없음', 
        '원피스', 
        '점프수트'
    ], 
    '상의 기장': [
        '없음', 
        '무릎 밑 기장', 
        '골반 기장', 
        '힙 기장', 
        '무릎 상의 기장', 
        '크롭 상의 기장'
    ], 
    '하의 기장': [
        '없음', 
        '7부 기장', 
        '크롭 팬츠 기장', 
        '미니 기장', 
        '롱 기장', 
        '무릎 하의 기장'
    ], 
    '여밈': [
        '없음', 
        '버튼', 
        '스트링', 
        '벨트', 
        '꼬임 장식', 
        '지퍼', 
        '버클', 
        '토글'
    ], 
    '브레스티드': [
        '없음', 
        '싱글 브레스티드', 
        '더블 브레스티드'
    ], 
    '패턴': [
        '없음', 
        '플로럴 패턴', 
        '무지 패턴', 
        '체크 패턴', 
        '기하학 및 비정형 패턴', 
        '스트라이프 패턴', 
        '도트 패턴', 
        '카모플라쥬 패턴'
    ], 
    '소매 기장': [
        '없음', 
        '긴팔', 
        '반팔', 
        '식별 불가', 
        '5부 소매', 
        '민소매', 
        '7부 소매'
    ], 
    '카라': [
        '없음', 
        '스탠드 카라', 
        '레귤러 카라', 
        '폴로 카라', 
        '오버사이즈 카라', 
        '노치드 카라', 
        '칼라리스'
    ], 
    '네크라인': [
        '없음', 
        '스파게티 스트랩', 
        '브이넥', 
        '라운드넥', 
        '스퀘어넥', 
        '하이넥', 
        '보트넥', 
        '오프숄더'
    ], 
    '후드': [
        '없음', 
        '후드'
    ], 
    '스커트 라인': [
        '없음', 
        'A라인 스커트', 
        'H라인 스커트', 
        '랩 스커트', 
        '핏 앤 플레어', 
        '플리츠 스커트', 
        '펜슬 스커트', 
        '티어드 스커트', 
        '머메이드 스커트'
    ], 
    '팬츠 라인': [
        '없음', 
        '스트레이트 팬츠', 
        '와이드 레그 팬츠', 
        '조거 팬츠', 
        '슬림 팬츠', 
        '스키니 팬츠', 
        '부츠컷 팬츠'
    ], 
    '핏': [
        '없음', 
        '슬림핏', 
        '레귤러핏', 
        '루즈핏', 
        '오버사이즈핏', 
        '타이트핏'
    ], 
    '웨이스트': [
        '없음', 
        '하이웨이스트', 
        '미드웨이스트', 
        '로우웨이스트'
    ], 
    '디테일': [
        '없음', 
        '절개', 
        '셔링 장식', 
        '로고', 
        '리본', 
        '레이스 장식', 
        '텍스트', 
        '픽처'
    ], 
    '주머니': [
        '없음', 
        '플랩 포켓', 
        '포켓', 
        '카고 포켓'
    ], 
    '소재': [
        '없음', 
        '니트', 
        '데님', 
        '퍼', 
        '울', 
        '레더', 
        '코듀로이', 
        '메쉬', 
        '패딩', 
        '골지 니트', 
        '트위드', 
        '스웨이드', 
        '합성 PVC'
    ], 
    'tpo': [
        '없음', 
        '파티', 
        '캐주얼', 
        '포멀', 
        '스포츠', 
        '홈앤라운지'
    ], 
    '스타일': [
        '없음', 
        '셋업', 
        '수트'
    ], 
    '연령대': [
        '없음', 
        '성인복', 
        '아동복'
    ], 
    '성별': [
        '없음', 
        '여성복', 
        '남성복'
    ], 
    '기타 의류 속성': [
        '없음', 
        '슬랙스', 
        '스웻팬츠', 
        '스웻셔츠', 
        '바람막이'
    ]
}