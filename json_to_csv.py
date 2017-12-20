import json

def load_to_json(fname="Output_exp.json"):
    with open(fname) as f:
        return json.loads(f.read())
hdrstr="id\t" \
       "Name\t" \
       "Age\t" \
       "Village #\t" \
       "sex\t" \
       "pre_active\t" \
       "pre_anxious\t" \
       "pre_cheerful\t" \
       "pre_exhausted\t" \
       "pre_lively\t" \
       "pre_restless\t" \
       "pre_tense\t" \
       "pre_unhappy\t" \
       "pre_worthless\t" \
       "pre_depressed_scale\t" \
       "pre_energetic_scale\t" \
       "pre_tired_scale\t" \
       "post_active\t" \
       "post_anxious\t" \
       "post_cheerful\t" \
       "post_exhausted\t" \
       "post_lively\t" \
       "post_restless\t" \
       "post_tense\t" \
       "post_unhappy\t" \
       "post_worthless\t" \
       "post_depressed_scale\t" \
       "post_energetic_scale\t" \
       "post_tired_scale"

fmtstr="{3}\t" \
       "{0}\t" \
       "{2}\t" \
       "{7}\t" \
       "{1}\t" \
       "{5[How active do you feel right now?]}\t" \
       "{5[How anxious do you feel right now?]}\t" \
       "{5[How cheerful do you feel right now?]}\t" \
       "{5[How exhausted do you feel right now?]}\t" \
       "{5[How lively do you feel right now?]}\t" \
       "{5[How restless do you feel right now?]}\t" \
       "{5[How tense do you feel right now?]}\t" \
       "{5[How unhappy do you feel right now?]}\t" \
       "{5[How worthless do you feel right now?]}\t" \
       "{5[On a scale from 1 to 10, how depressed do you feel right now?]}\t" \
       "{5[On a scale from 1 to 10, how energetic do you feel right now?]}\t" \
       "{5[On a scale from 1 to 10, how tired do you feel right now?]}\t" \
       "{6[How active do you feel right now?]}\t" \
       "{6[How anxious do you feel right now?]}\t" \
       "{6[How cheerful do you feel right now?]}\t" \
       "{6[How exhausted do you feel right now?]}\t" \
       "{6[How lively do you feel right now?]}\t" \
       "{6[How restless do you feel right now?]}\t" \
       "{6[How tense do you feel right now?]}\t" \
       "{6[How unhappy do you feel right now?]}\t" \
       "{6[How worthless do you feel right now?]}\t" \
       "{6[On a scale from 1 to 10, how depressed do you feel right now?]}\t" \
       "{6[On a scale from 1 to 10, how energetic do you feel right now?]}\t" \
       "{6[On a scale from 1 to 10, how tired do you feel right now?]}"
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
                print(fmtstr.format(*person,vill_n))
            except KeyError:
                errs+=1
    print("\n\n\nERROR COUNT",errs)