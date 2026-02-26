import json
from ast import literal_eval
import pandas as pd
import llm_extract_orgs


# constants
PATH_TO_CSV = ""  # scientific publication dataset path
PATH_OUTPUT_DATA = ""  # where to save the .json map of orgs to extracted orgs

def main():
    df = pd.read_csv(PATH_TO_CSV)
    df['Affiliations'] = df['Affiliations'].apply(lambda x : literal_eval(x))
    df['Affiliations'] = df['Affiliations'].split('; ')
    aff_list = []
    for i in df['Affiliations']:
        for j in i:
            aff_list.append(j)
    out = llm_extract_orgs.batch_canonicalize(aff_list)
    with open(PATH_OUTPUT_DATA, 'w') as f:
        json.dump(out, f)

if __name__ == "__main__":
    main()
# EOF