import re
import ast

case_to_handle = """Hello! It seems like you might be looking for a property, but I could use a bit more information. Could you please share your property requirements and preferences? For example, let me know your budget, the number of bedrooms and bathrooms you're looking for, or any other specific features that are important to you.

```python
user_criteria = {}
information_complete = False
```
"""


def clean_response(result):
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


# Call the function with the text to handle
chat_for_user = clean_response(case_to_handle)


print("Chat for user:", chat_for_user)
