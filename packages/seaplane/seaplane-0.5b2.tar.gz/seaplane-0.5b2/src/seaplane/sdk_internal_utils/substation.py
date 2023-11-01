from typing import Any, Optional

import requests

from seaplane.config import config
from seaplane.sdk_internal_utils.http import headers
from seaplane.sdk_internal_utils.token_auth import method_with_token


class SubstationAPI:
    """
    Class for handle Substation API calls.
    """

    def __init__(self) -> None:
        pass

    # This is the template that works best with the mpt-30b-instruct model;
    # strongly advised to use this format.
    # TODO: Generalize this to support other models
    def _format_prompt(self, instruction: str) -> str:
        template = "Below is an instruction that describes a task. Write a response that appropriately completes the request.\n\n###Instruction\n{instruction}\n\n### Response\n"  # noqa
        return template.format(instruction=instruction)

    @method_with_token
    def predict(
        self,
        token: str,
        prompt: str,
        max_output_length: Optional[int] = 3000,
        model_specific_prompt: Optional[bool] = True,
    ) -> Any:
        if model_specific_prompt:
            prompt = self._format_prompt(prompt)
        url = f"{config.substation_endpoint}/completions"
        res = requests.post(
            url,
            headers=headers(token),
            json={"max_tokens": max_output_length, "prompt": prompt},
        )
        res.raise_for_status()
        if res.headers.get("content-type") == "application/octet-stream":
            return res.content
        else:
            return res.json()
