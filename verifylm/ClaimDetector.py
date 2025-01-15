import openai
from pydantic import BaseModel


class ClaimsResponseObject(BaseModel):
    claims: list[str]


class ClaimDetector:
    def __init__(self, openai_api_key: str) -> None:
        self.system_prompt = """
            I will provide you with a written text. Identify any factual claims contained within the text, and extract them.

            A claim is a factual part of a sentence that can be fact checked to determine it to be true or false by gathering evidence from an external source. There are many different types of claims: claims about quantities (e.g. "GDP has risen by 5%"), claims about cause and effect (e.g. "this policy leads to econimic growth"), historical claims (e.g. "the prime minister cut the education budget by £5bn in 2023"), or predictive claims about the future (e.g. "economists say this will cost working people $100 more per year").

            Identified claims should be an exact quote from the text. Ensure to only include relevant and substantial claims that are verifiable and not opinion or sarcasm.

            Use the context of the entire text to help identify where claims are.

            If the claim makes reference to someone or something (e.g. "he said"), search backwards in the text to identify the subject being referenced (e.g. "Rishi Sunak"), and replace the reference within the claim with the named subject.

            You should respond with an array containing any extracted claims from the entire. If no claims are found, return any empty array.

            Example 1:
            * Sentence from text: "I tell you Stephen, this year alone 10,000 people have crossed on boats, that's a record number, so again, he's made a promise and he's completely failed to keep it."
            * Output claims: ["this year alone, 10,000 people have crossed on boats"]

            Example 2:
            * Sentence from text: "We need to smash the gangs that are running this file trade making a huge amount of money."
            * Output claims: []

            Example 3:
            * Sentence from text: "Donald Trump is unburdened unburdened by the truth. He said the neo nazi rally in Charlottesville was fabricated."
            * Output claims: ["Donald Trump said the neo nazi rally in Charlottesville was fabricated"]
        """

        self.base_user_prompt = "This is the input transcript to extract claims from:"

        # Set up connection to OpenAI API
        self.openai = openai.OpenAI(api_key=openai_api_key)

    def run(self, input_text: str) -> list[str]:
        # Define prompt for OpenAI model to extract claims from input text
        user_prompt = self.base_user_prompt + "\n" + input_text

        # Send prompt & retrieve response from OpenAI model
        try:
            response = self.openai.beta.chat.completions.parse(
                messages=[
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": user_prompt},
                ],
                model="gpt-4o",
                response_format=ClaimsResponseObject,
            )
        except openai.OpenAIError as error:
            print(f"<!> ERROR: '{error.body['message']}'. Cannot get response from OpenAI. <!>")
            return []

        # Extract array of claims from OpenAI response
        detected_claims = response.choices[0].message.parsed.claims

        return detected_claims
