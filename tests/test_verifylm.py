import json

import pytest

from verifylm.VerifyLM import VerifyLM


def test_api_keys_exist():
    with open("verifylm/credentials.json", "r") as file:
        CREDENTIALS = json.load(file)

    keys_to_check = ["google_api_key", "openai_api_key"]

    for key_name in keys_to_check:
        assert key_name in CREDENTIALS.keys()

        key_value = CREDENTIALS[key_name]

        assert key_value is not None and key_value != ""


@pytest.fixture
def verifylm():
    with open("verifylm/credentials.json", "r") as file:
        credentials = json.load(file)
        GOOGLE_API_KEY = credentials["google_api_key"]
        OPENAI_API_KEY = credentials["openai_api_key"]

    verifylm = VerifyLM(GOOGLE_API_KEY, OPENAI_API_KEY)

    return verifylm


def test_trump_dogs(verifylm):
    text = "During ABC's presidential debate, Trump said: 'In Springfield, they are eating the dogs. The people that came in, they are eating the cats. They're eating - they are eating the pets of the people that live there.' But city officials have told BBC Verify there have been 'no credible reports' that this has actually happened."

    output = verifylm.run(text)

    assert len(output) > 0
    assert len(output[0]["factCheckResults"][0]["claimReview"]) > 0
