import re
from .token import get_rule_from_yaml

def parse_gpt_answer(gpt_answers:list)->dict:
    """
    gpt 생성 결과를 key-value쌍으로 parsing
      예) {'제품명':'울 체크 기본핏 재킷', ...}
    """
    answer_dict = dict()
    for answer in gpt_answers: 
        # "1. 제품명 : 울 체크 기본핏 재킷" -> ('제품명', '울 체크 기본핏 재킷')
        match = re.match(r"\s*\d+[.]\s*(.+)[:]\s*(.+)", answer)
        if match != None:
            key, value = match.groups()    
            key = key.replace(" ","")
            answer_dict[key] = value
    return answer_dict

def get_gpt_content_by_dict(gpt_answers:list)-> dict:
    """
    gpt 생성 결과를 피그마 템플릿 변수명으로 매핑
      예)  {"prod-name-kr": "울 체크 기본핏 재킷", ...} 
    """
    gpt_answers = parse_gpt_answer(gpt_answers)
    template_label_dict = get_rule_from_yaml('template_label_dict')

    gpt_answer_dict = dict()
    for key, value in template_label_dict.items():
        if value in gpt_answers.keys():
            gpt_answer_dict[key]=gpt_answers[value]
        else:
            gpt_answer_dict[key]=''

    return gpt_answer_dict

def change_expressions(gpt_answer):
    """
    gpt 생성 결과 후처리 로직
    - gpt가 생성한 단어를 다른 표현으로 바꿈
    """
    word_changes = get_rule_from_yaml("word_changes")
    for src, dst in word_changes:
        gpt_answer = gpt_answer.replace(src, dst)
    return gpt_answer