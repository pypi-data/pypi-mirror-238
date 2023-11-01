import os
import json
import yaml
import pandas as pd

# Paths
root_path = os.path.dirname(os.path.abspath(__file__))
src_path = os.path.join(root_path, "src")
csv_path = os.path.join(src_path, "mlft_kor.csv")

# mlft_kor
sclass_df = pd.read_csv(csv_path, usecols=[0, 1])
sclass_df = sclass_df.dropna(axis=0)

attr_df = pd.read_csv(csv_path, usecols=[2, 3])

# kor answer
sclass_kor_dict = dict(zip(sclass_df['superclass'].to_list(), sclass_df['superclass_kr'].to_list()))
attr_kor_dict = dict(zip(attr_df['attribute'].to_list(), attr_df['attribute_kr'].to_list()))

def get_prompts(path=os.path.join(src_path, "gpt_prompts.json")):
    if not os.path.exists(path):
        #TODO: Download from S3
        raise NotImplementedError
    with open(path, "r", encoding="utf-8") as f:
        prompts = json.load(f)
    return prompts


def get_category_info(product_point: dict):
    """
    mlft 결과로부터 카테고리 정보 추출
    """
    category_superclass = get_rule_from_yaml("category_superclass")
    for superclass, attribute in product_point.items():
        if superclass in category_superclass:
            category = attribute
            return category

def get_rule_from_yaml(key, path=os.path.join(src_path, "rules.yaml")):
    """get variables from src/rules.yaml"""
    with open(path, encoding="utf-8") as f:
        rules = yaml.load(f, Loader=yaml.FullLoader)
    return rules[key]