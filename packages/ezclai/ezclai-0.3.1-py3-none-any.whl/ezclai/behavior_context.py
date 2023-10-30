from dataclasses import dataclass
from typing import Literal, Union

from ezclai.ocr_drivers import WindowContext
from ezclai.ocr_drivers.base_driver import ClipboardContext

USER_PROMPT_FORMAT = """
User Prompt:
```
{user_prompt}
```
"""
OCR_EXTRACTION_FORMAT = """
Active Window Title: {active_window_title}

Active Window OCR Extracted Text (RAW):
------ OCR DATA START ------
```
{ocr_text}
```
------ OCR DATA END ------

{user_prompt}

Please answer "User Prompt" using the raw OCR text as context to the message.
"""

CLIPBOARD_EXTRACTION_FORMAT = """
Clipboard Text:
```
{clipboard_text}
```
Clipboard Text End:


{user_prompt}

Please answer "User Prompt" using the clipboard text as context to the message.
"""


@dataclass
class Prompt:
    context: WindowContext
    prompt: str

    def __str__(self) -> str:
        """Serialize the Prompt with differing formats, depending on whether window
        content was available

        :return: The window context and prompt in a standardized format
        """
        """."""
        user_prompt = USER_PROMPT_FORMAT.format(user_prompt=self.prompt.strip())
        if self.context:
            if isinstance(self.context, WindowContext) and self.context.clean_screen_text and self.context.active_window_name:
                return OCR_EXTRACTION_FORMAT.format(
                    active_window_title=self.context.active_window_name.strip(),
                    ocr_text=self.context.clean_screen_text.strip(),
                    user_prompt=user_prompt.strip(),
                )
            elif isinstance(self.context, ClipboardContext) and self.context.text:
                return CLIPBOARD_EXTRACTION_FORMAT.format(
                    clipboard_text=self.context.text.strip(),
                    user_prompt=user_prompt.strip(),
                )
                
        return user_prompt.strip()


@dataclass
class Message:
    role: Literal["system", "user", "assistant"]
    content: Union[Prompt, str]

    def to_api(self) -> dict[str, str]:
        """To OpenAPI format"""
        if isinstance(self.content, str) and self.role == "user":
            raise RuntimeError("The user message must be of type Prompt!")

        return {"role": self.role, "content": str(self.content)}


_DEFAULT_ASSISTANT_ROLE = """
You are an assistant that is capable of being called anywhere on a desktop computer. You
may be called within the context of an email, a URL box, commandline, a text editor, or
even word documents!

Your role is to answer the users request as shortly and succinctly as possible. You
will follow the following rules:

When asked to write long-form text content:
1) Never ask for more information. If something is to be guessed, write it in template
   format. For example, if asked to write an email use <Insert time here> when writing
   the portion of an email that specifies something that was not included in the users
   question.
2) Only assume the content is long form if the user mentions email, or 'long message'.

When asked to write a command, code, formulas, or any one-line response task:
1) NEVER WRITE EXPLANATIONS! Only include the command/code/etc, ready to be run
2) NEVER WRITE USAGE INSTRUCTIONS! Do not explain how to use the command/code/formulas.
3) NEVER WRITE NOTES ABOUT THE IMPLEMENTATION!
   Do not explain what it does or it's limitations.
4) Remember, the text that you write will immediately be run, do not include code blocks
5) If there is something that requires user input, such as a cell in a sheet or a
   variable from the user, write it inside of brackets, like this: <INPUT DESCRIBER>,
   where the insides of the bracket have an example of what is needed to be filled in.
6) Assume a linux desktop environment in a bash shell. Use freely available unix tools.

You will receive OCR context and window title names, for some prompts. They are very
noisy, use best-effort when reading them.
"""

MESSAGE_CONTEXT: list[Message] = [
    Message(role="system", content=_DEFAULT_ASSISTANT_ROLE),    
]

__all__ = ["MESSAGE_CONTEXT", "Message", "Prompt"]
