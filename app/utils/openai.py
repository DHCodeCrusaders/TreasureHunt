import json
from os import environ

import openai
from loguru import logger


class OpenAi:
    def __init__(self, token: str, model_name: str = "gpt-3.5-turbo"):
        self.model_name = model_name
        self.token = token
        self.openai = openai
        self.openai.api_key = self.token

    def _parse_response(self, response):
        try:
            return json.loads(response.choices[0].message.content)
        except Exception as err:
            logger.error(
                "Error parsing GPT response. Response: {} Error: {}".format(
                    response, err
                )
            )
            return {"error": "Something went wrong."}

    def riddle_generate(self):
        prompt = """
        You are a riddle generator AI. Generate a riddle, some hints and its answer.

        The output should be in a JSON format and nothing else. Eg:

        {"riddle": <riddle>, "hints": [<hint1>, <hint2>, ...], "answer": <answer>}
        """
        response = self.openai.ChatCompletion.create(
            model=self.model_name,
            messages=[
                {
                    "role": "system",
                    "content": prompt,
                },
            ],
        )

        return self._parse_response(response)

    def riddle_verify(self, riddle, answer, user_answer):
        logger.info(
            f"Riddle verification Riddle: {riddle} | Answer: {answer} | user answer: {user_answer}"
        )
        prompt = """
        You are a riddle answer checker AI. You are given with a riddle, its answer and a user answer.
        Check if the user answer is correct or not.

        The output should be in a JSON format. No thing else and no explanation.
        If the answer is correct, message should be empty. If the answer is wrong, give the accuracy score.
        Like: You are nearly correct, think better etc
        Eg:
        {{"correct": true, "message": ""}}
        {{"correct": false, "message": "<conclusion>"}}

        Given riddle: {riddle}
        Given answer: {answer}
        Given user answer: {user_answer}
        """.format(
            riddle=riddle,
            answer=answer,
            user_answer=user_answer,
        )
        response = self.openai.ChatCompletion.create(
            model=self.model_name,
            messages=[
                {
                    "role": "system",
                    "content": prompt,
                },
            ],
        )

        return self._parse_response(response)


logger.info("Initializing OpenAI")
gpt = OpenAi(environ.get("OPENAI_TOKEN"))
