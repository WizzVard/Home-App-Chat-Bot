import re
import ast

case_to_handle = """
('wef', "Hello! I'm here to assist you in finding your ideal home. Could you please share what type of property you're looking for, along with any key requirements or personal preferences that are important to you? This will help me narrow down the options and find the best matches for you! \n\nuser_criteria = {}\ninformation_complete = False")
"""
case_to_handle_2 = """
Hello! It seems like you might be looking for a property, but I could use a bit more information. Could you please share your property requirements and preferences? For example, let me know your budget, the number of bedrooms and bathrooms you're looking for, or any other specific features that are important to you.

```python
user_criteria = {"a": 1}
information_complete = True
```
"""


def extract_criteria(last_history):
    # Extract user_criteria and information_complete from last_history
    criteria_pattern = r"\**user_criteria\s*=\s*(\{.*?\})\**"
    complete_pattern = r"\**information_complete\s*=\s*(\w+)\**"

    # Use re.DOTALL to match across multiple lines
    criteria_match = re.search(criteria_pattern, last_history, re.DOTALL)
    complete_match = re.search(complete_pattern, last_history)

    user_criteria = {}
    information_complete = False

    if criteria_match:
        # criteria_string = "{" + criteria_match.group(1) + "}"
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


# Call the function with the text to handle
user_criteria, information_complete = extract_criteria(case_to_handle_2)


print("User Criteria:", user_criteria)
print("Information Complete:", information_complete)