import requests


class FactChecker:
    def __init__(self, google_api_key: str) -> None:
        self.gfc_api_key = google_api_key

        self.claim_language = "en"
        self.fact_check_api = "https://factchecktools.googleapis.com/v1alpha1/claims:search"

        self.rating_terms_mapping = {
            "Pants on Fire": "False",
            "One Pinocchio": "Mostly true: some omissions and exaggerations, but no outright falsehoods.",
            "Two Pinocchios": "Half true: significant omissions and/or exaggerations.",
            "Three Pinocchios": "Mostly false: significant factual error and/or obvious contradictions.",
            "Four Pinocchios": "False",
            "Geppetto Checkmark": "True",
            "Verdict Pending": "Verdict pending: judgement cannot be fully rendered",
        }

    def run(self, claims: list[str]) -> list[dict]:
        # Parameters and variables
        params = {"key": self.gfc_api_key, "languageCode": self.claim_language, "query": ""}
        fact_checked_claims = []

        for claim in claims:
            # Call Google Fact Check API to match input claim to known fact-checked claims
            params["query"] = claim
            response = requests.get(url=self.fact_check_api, params=params)

            response = response.json()
            fact_check_output = []

            if response != {}:
                gfc_results = response["claims"]

                # Constrict output to only top 3 sources
                if len(gfc_results) > 3:
                    gfc_results = gfc_results[:3]

                # Extract relevant fact-check info from response and format into output data structure
                for result in gfc_results:
                    fact_check_object = {
                        "factCheckMethod": "Google Fact Check",
                        "matchedClaim": result["text"] if "text" in result.keys() else None,
                        "claimSimilarity": None,
                        "matchedClaimSpeaker": result["claimant"] if "claimant" in result.keys() else None,
                        "publishingDate": None,
                        "claimReview": result["claimReview"] if "claimReview" in result.keys() else None,
                    }

                    fact_check_output.append(fact_check_object)

            checked_claim = {"claimText": claim, "factCheckResults": fact_check_output}
            fact_checked_claims.append(checked_claim)

        return fact_checked_claims
