import logging

from verifylm.ClaimDetector import ClaimDetector
from verifylm.FactChecker import FactChecker

logger = logging.getLogger(__name__)


class VerifyLM:
    def __init__(self, google_api_key: str, openai_api_key: str) -> None:
        self.detector = ClaimDetector(openai_api_key)
        self.checker = FactChecker(google_api_key)

    def run(self, text: str):
        # Data structures & variables
        fact_checked_claims = []

        # Use OpenAI GPT model to detect & extract claims in the text
        detected_claims = self.detector.run(text)
        logger.info(detected_claims)

        # Claim verification using Google Fact Check or Google search & OpenAI summary
        fact_checked_claims = self.checker.run(detected_claims)

        return fact_checked_claims
