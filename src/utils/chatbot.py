from typing import List
from src.utils.improved_chain import Neo4jChain
from src.utils.load_openai import generate_response
import re
import ast
from src.utils.load_config import LoadConfig

CONFIG = LoadConfig()


class ChatBot:
    """
    This class executes main functionality of a chatbot including:
    a) Generates first conversation with user
    b) Extracts main criteria from user's request
    c) Cleans llm response for the user
    d) Generates final summary response based on found criteria
    """
    def __init__(self):
        self.history_for_llm = []
        self.clear_history = False

    @staticmethod
    def extract_criteria(sec_history):
        """
        This function extracts criteria from user's request
        :param sec_history: history for llm
        :return:
            user_criteria: Dictionary with extracted criteria
            information_complete: Flag that becomes True if LLM changed it to True.
            It happens if llm decides that user gave all necessary criteria.
        """
        # Extract last history from history for llm
        last_history = str(sec_history[-1])

        # Extract user_criteria and information_complete from last_history
        criteria_pattern = r"\**user_criteria\s*=\s*(\{.*?\})\**"
        complete_pattern = r"\**information_complete\s*=\s*(\w+)\**"

        # Use re.DOTALL to match across multiple lines
        criteria_match = re.search(criteria_pattern, last_history, re.DOTALL)
        complete_match = re.search(complete_pattern, last_history)

        user_criteria = {}
        information_complete = False

        if criteria_match:
            criteria_string = criteria_match.group(1)
            # Clean up the string by removing newlines and extra spaces
            criteria_string = criteria_string.replace("\n", "").replace("\\n", "")
            # Use ast.literal_eval for safe evaluation
            try:
                user_criteria = ast.literal_eval(criteria_string)
            except (SyntaxError, ValueError) as e:
                print(f"Error parsing user_criteria: {e}")

        if complete_match:
            information_complete = complete_match.group(1) == "True"

        return user_criteria, information_complete

    @staticmethod
    def clean_response(result):
        """
        This function cleans LLM response from user_criteria dictionary and information_complete flag in the end.
        :param result: Generated llm response that includes user_criteria dictionary and information_complete flag
        :return: chat_for_user: Cleaned llm response from user_criteria dictionary and information_complete flag
        """
        # Flags to indicate if inside user_criteria block or code block
        cleaned_lines = []
        in_criteria_block = False
        in_code_block = False

        # Iterate through lines and remove user_criteria block and code block
        for line in result.split("\n"):
            stripped_line = line.strip()

            # Check for user_criteria block
            if stripped_line.startswith("user_criteria"):
                in_criteria_block = True
            elif in_criteria_block and stripped_line == "}":
                in_criteria_block = False
                continue

            # Check for code block
            if stripped_line.startswith("```python"):
                in_code_block = True
                # Skip the opening of the code block
                continue
            elif in_code_block and stripped_line.startswith("```"):
                in_code_block = False
                # Skip the closing of the code block
                continue

            # Append line if not in any block
            if not in_criteria_block and not in_code_block and not stripped_line.startswith("information_complete"):
                cleaned_lines.append(line)

        # Remove the last line if present
        if cleaned_lines and (in_code_block or in_criteria_block):
            # Ensure the last line is removed regardless of content
            cleaned_lines.pop(-1)

        # Remove the last line if it starts with "Here"
        if cleaned_lines and cleaned_lines[-1].strip().startswith("Here") and (in_code_block or in_criteria_block):
            cleaned_lines.pop()

        # Construct the chat_for_user without user_criteria or information_complete
        chat_for_user = "\n".join(cleaned_lines)
        return chat_for_user

    def clear_second_history(self, flag):
        """This function changes the flag to True if the clear button was clicked."""
        if flag:
            self.clear_history = True

    def respond(self, chatbot: List, message: str):
        """
        This function combines all the functionality of the chatbot.
        :param chatbot: History of the chat with user and llm
        :param message: Last message from user
        :return: Returns empty string that is llm response and a chatbot response
        """
        # If clear button was pressed, clear all the history for llm
        if self.clear_history:
            self.history_for_llm = ['']
            self.clear_history = False

        conversation_message = CONFIG.system_message_extract
        llm_message = conversation_message.format(chat_history=self.history_for_llm)

        user_prompt = (
            "### User Prompt ###\n"
            f"{message}\n"
            "### Response ###\n"
        )

        # Generate llm response to collect all user's criteria
        result = generate_response(llm_message, user_prompt)

        # Add full generated response to llm_history
        self.history_for_llm.append((message, result))

        # Extract last chat with user history to decide if the flag information_complete is True
        last_history = str(self.history_for_llm[-1])

        # Extract user_criteria dict and information_complete flag
        user_criteria, information_complete = self.extract_criteria(self.history_for_llm)

        # Extract cleaned generated response for chat with user
        chat_for_user = self.clean_response(result)

        # Add cleaned generated response for chat with user
        chatbot.append((message, chat_for_user))

        # Check if all is good
        print(f"History for user: {chatbot}")
        print(f"History for llm: {self.history_for_llm}")
        print(f"History list contains {len(self.history_for_llm)} elements")
        print(f"Last history: {last_history}")
        print(f"Extracted user_criteria: {user_criteria}")
        print(f"Extracted information_complete: {information_complete}")
        print(f"Chat for user: {chat_for_user}")

        # If information is complete, generate final summary response
        if information_complete:
            neo4j_results = Neo4jChain().home_app_response(user_criteria)
            print("Neo4j Results:", neo4j_results)
            final_result = generate_response(CONFIG.final_system_message, neo4j_results)

            chatbot.append((message, final_result))

        return "", chatbot
