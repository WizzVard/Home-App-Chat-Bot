from dotenv import load_dotenv
from src.utils.load_config import LoadConfig

load_dotenv()

CONFIG = LoadConfig()


def generate_response(llm_role, user_prompt):
    """
    This function generates a response based on the llm role and user input
    :param llm_role: system role of LLM
    :param user_prompt: prompt from user
    :return: Generated response
    """
    llm_response = CONFIG.client.chat.completions.create(
        model=CONFIG.model_name,
        messages=[
            {"role": "system", "content": llm_role},
            {"role": "user", "content": user_prompt}
        ]
    )
    response = llm_response.choices[0].message.content

    return response
