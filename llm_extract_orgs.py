from openai import OpenAI
import time

# constants
MODEL = ""  # pick a model, we use openAI's gpt4o-mini, it is perfect for this task, and cheap (< $1USD / 42k org extractions)

SYSTEM_PROMPT = """
You standardize scientific affiliation strings for bibliometric network analysis.

Extract the highest-level SEMI-INDEPENDENT institution name only.

Rules:
- Remove departments, faculties, schools, laboratories, research centers.
- Remove street addresses and postal codes.
- If both an institute and its umbrella organization appear,
  return the institute.
- If only the umbrella organization appears, return it.
- Extract: Full Name (Abbreviation), City, Country.
- If uncertain, return null.
- Do not explain.
"""

# examples for few shot learning
FEW_SHOTS = [
    {
        "role": "user",
        "content": "Department of Physics, Massachusetts Institute of Technology, Cambridge, MA, USA"
    },
    {
        "role": "assistant",
        "content": "Massachusetts Institute of Technology"
    },
    {
        "role": "user",
        "content": "School of Medicine, University of Tokyo, Japan"
    },
    {
        "role": "assistant",
        "content": "University of Tokyo"
    },
    {
        "role": "user",
        "content": "Key Laboratory of Space Active Opto-Electronics Technology, Shanghai Institute of Technical Physics, Chinese Academy of Sciences, Shanghai, China"
    },
    {
        "role": "assistant",
        "content": "Shanghai Institute of Technical Physics"
    },
    {
        "role": "user",
        "content": "Key Laboratory of Space Active Opto-Electronics Technology, Chinese Academy of Sciences, Shanghai, China"
    },
    {
        "role": "assistant",
        "content": "Chinese Academy of Sciences"
    }
]

# functions
def call_model(raw_affiliation):
    client = OpenAI()
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    messages.extend(FEW_SHOTS)
    messages.append({"role": "user", "content": raw_affiliation})
    response = client.chat.completions.create(
        model=MODEL,
        temperature=0,  # set to 0 -> more deterministic
        messages=messages
    )
    return response.choices[0].message.content.strip()

def batch_canonicalize(affiliations):
    results = {}
    for aff in set(affiliations):  # deduplicate to save cost
        print("Processing:", aff)
        canonical = call_model(aff)
        results[aff] = canonical
        time.sleep(0.2)  # mild rate-limit safety
    return results
# EOF