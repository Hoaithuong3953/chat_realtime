from dataclasses import dataclass

@dataclass(frozen=True)
class AIDetectorResult:
    detected: bool
    input: str | None = None

class AIDetector:
    TRIGGER = "@ai"

    @staticmethod
    def detect(text_content: str | None) -> AIDetectorResult:
        # Check if the content after the strip must not be empty
        if not text_content:
            return AIDetectorResult(detected=False)

        text_content = text_content.strip()

        # Check if the trigger is at the beginning of the message
        if not text_content.lower().startswith(AIDetector.TRIGGER):
            return AIDetectorResult(detected=False)

        # Check if the character immediately following the trigger is a whitespace
        if len(text_content) > len(AIDetector.TRIGGER):
            next_char = text_content[len(AIDetector.TRIGGER)]

            if not next_char.isspace():
                return AIDetectorResult(detected=False)

        # Get the input after the trigger
        ai_input = text_content[len(AIDetector.TRIGGER):].strip()

        # Check if the input is not empty
        if not ai_input:
            return AIDetectorResult(detected=False)

        return AIDetectorResult(
            detected=True,
            input=ai_input,
        )