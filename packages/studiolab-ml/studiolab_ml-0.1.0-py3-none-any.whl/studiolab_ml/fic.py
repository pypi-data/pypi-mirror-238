import os
import openai

# import logging
from studiolab_ml.common import package_root, verify_model
from .fic_utils import *

# logging.basicConfig(level=logging.debug)


class FIC:
    model_urls = {
    '1.0': {
        "model": "gpt-3.5-turbo",
        "prompt": {
            "local": os.path.join(package_root, "fic_utils/src/gpt_prompts.json"),
            "url": "fic/gpt_prompts.json"
        }
    }
}

    def __init__(
            self,
            version: str = '1.0',
            use_gpu: bool = False, # Dummy now
            api_key: str = None,            
            aws_access_key_id: str = None,
            aws_secret_access_key: str = None,
            temperature: float = 0.1,
        ):
        openai.api_key = api_key
        self.model = self.model_urls[version]
        _ = verify_model(self.model, aws_access_key_id, aws_secret_access_key, prompt=True)
        self.logit_bias=get_logit_bias()
        self.prompts = get_prompts()
        self.temperature = temperature 


    def __call__(
            self,
            main_attributes: dict, 
            user_input_info: dict
    ):


        request_content = self.get_request_content(main_attributes, user_input_info)

        # Call GPT
        completion = openai.ChatCompletion().create(
            model= self.model,
            messages=[
                {"role": "system", "content": request_content["system"]},
                {"role": "user", "content": request_content["input_example"]},
                {"role": "assistant", "content": request_content["output_example"]},
                {"role": "user", "content": request_content["user_input"]},
            ],
            stop="컬러 요약",
            logit_bias=self.logit_bias,
            temperature=self.temperature,
        )

        # Extract Answer
        answer = completion["choices"][0]["message"]["content"]
        answer = change_expressions(answer)

        # # Token Usage Calculation : Not used now
        # prompt = (
        #     request_content["system"]
        #     + request_content["input_example"]
        #     + request_content["output_example"]
        #     + request_content["user_input"]
        # )
        # count_token_usage(prompt, answer)

        answer = answer.split("\n\n")
        answer = answer[0].split("\n")
        return answer
    
    def get_request_content(
            self, 
            product_point: dict, 
            product_info: dict
    ) -> dict:
        """
        최종 gpt 호출 프롬프트 생성
        """
        category = get_category_info(product_point)

        if "nick_name" in product_point.keys():
            nickname = product_point["nick_name"]
        else:
            nickname = f'{product_info["color_name"]} {category}'  # ex) 브라운 재킷

        user_input = get_request_product_info(product_info, nickname) + get_request_product_point(product_point)

        content = {
            "system": self.prompts["system"],
            "input_example": self.prompts["example"][category]["input"],
            "output_example": self.prompts["example"][category]["output"],
            "user_input": user_input,
        }
        return content
