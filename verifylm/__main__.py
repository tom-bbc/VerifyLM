import json
import logging

from VerifyLM import VerifyLM

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

with open("verifylm/credentials.json", "r") as file:
    CREDENTIALS = json.load(file)

GOOGLE_API_KEY = CREDENTIALS["google_api_key"]
OPENAI_API_KEY = CREDENTIALS["openai_api_key"]

logger.info("Started")
verifylm = VerifyLM(GOOGLE_API_KEY, OPENAI_API_KEY)

# text = "A marginal dip in the headline rate of inflation would not normally determine much, if anything. Inflation rising at 2.5% rather than 2.6% does not change much in big economics, nor in the cost of living squeeze felt by households. The fall is entirely accounted for by falls in hotel prices and a smaller-than-usual rise in airfares in December. But this unusually important 0.1% drop signals relief, and some respite for Chancellor Rachel Reeves, because of what underpins it. The underlying inflation numbers, which show where price pressures are going over the year, are what is most keenly watched by the Bank of England in terms of interest rate cuts. Core inflation, which strips out the direct impact of volatile energy and food prices is now at a four-year low, having dropped to 3.2% in December from 3.5%. Services inflation is at a two-year low of 4.4% after a chunky fall from 5%. This is the real positive news."
text = "During ABC's presidential debate, Trump said: 'In Springfield, they are eating the dogs. The people that came in, they are eating the cats. They're eating - they are eating the pets of the people that live there.' But city officials have told BBC Verify there have been 'no credible reports' that this has actually happened."

output = verifylm.run(text)

logger.info(json.dumps(output, indent=4))
logger.info("Finished")
