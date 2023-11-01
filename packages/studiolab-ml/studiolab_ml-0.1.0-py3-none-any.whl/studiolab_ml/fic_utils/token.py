import os

import tiktoken

from .meta import get_rule_from_yaml

# GPT token encoder for getting token ids
encoder = tiktoken.get_encoding("cl100k_base")


def get_logit_bias():
    """
    특정 토큰에 대한 logit bias 생성
    - logit bias: 특정 토큰이 생성될 확률을 통제
    """
    logit_bias = dict()

    negative = get_rule_from_yaml("negative_tokens")
    positive = get_rule_from_yaml("positive_tokens")

    # nagative tokens
    token_ids = set()
    for word in negative:
        token_ids.update(encoder.encode(word))
    for id in token_ids:
        logit_bias[id] = -100

    # positive tokens
    token_ids = set()
    for word in positive:
        token_ids.update(encoder.encode(word))
    for id in token_ids:
        logit_bias[id] = 3

    return logit_bias


def count_token_usage(input, output, model="gpt-3.5-turbo"):
    """
    gpt 입출력에 사용된 토큰 수 계산
    """
    input_token = len(encoder.encode(input))
    output_token = len(encoder.encode(output))
    total_token = input_token + output_token

    if model == "gpt-3.5-turbo":
        cost = 0.0015 * (input_token / 1000)
        cost += 0.002 * (output_token / 1000)
        # logging.debug('[FIC] token usage: %d tokens, $%.4f' %(total_token, cost))
    else:
        cost = 0.0  # not calculated
    return {"token_usage": total_token, "cost": cost}
