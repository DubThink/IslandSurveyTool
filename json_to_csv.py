import json

def load_to_json(fname="Output_exp.json"):
    with open(fname) as f:
        return json.loads(f.read())
hdrstr="id\tName\tAge\tVillage #\tsex\tpre_energetic\tpre_lively\tpre_anxious\tpre_cheerful\tpre_worthless\tpre_exhausted\tpre_restless\tpre_tired\tpre_active\tpost_energetic\tpost_lively\tpost_anxious\tpost_cheerful\tpost_worthless\tpost_exhausted\tpost_restless\tpost_tired\tpost_active"
fmtstr="{3}\t{0}\t{2}\t{7}\t{1}\t{5[energetic]}\t{5[lively]}\t{5[anxious]}\t{5[cheerful]}\t{5[worthless]}\t{5[exhausted]}\t{5[restless]}\t{5[tired]}\t{5[active]}\t{6[energetic]}\t{6[lively]}\t{6[anxious]}\t{6[cheerful]}\t{6[worthless]}\t{6[exhausted]}\t{6[restless]}\t{6[tired]}\t{6[active]}"
def run(json):
    errs=0
    print(hdrstr)
    for vill_n in json:
        vill=json[vill_n]
        # print(vill)
        for person in vill:
            person.append(vill_n)
            #print(person)
            try:
                print(fmtstr.format(*person))
            except KeyError:
                errs+=1
    print("\n\n\nERROR COUNT",errs)