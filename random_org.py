import requests, json
import keys

# inclusive
def org_randint(min,max,ct):
    data={
        "jsonrpc": "2.0",
        "method": "generateIntegers",
        "params": {
            "apiKey": keys.ic_api_key,
            "n": ct,
            "min": min,
            "max": max,
            "replacement": True
        },
        "id": 42
    }
    #return int(requests.get("https://www.random.org/integers/?num=1&min=1&max={}&col=1&base=10&format=plain&rnd=new".format(a)).content)
    # todo digest return using json and reply with values.
    # todo use params for the count of numbers
    j=json.loads(requests.post("https://api.random.org/json-rpc/1/invoke",json=data).content.decode("utf-8"))
    return j["result"]["random"]["data"]

# if __name__ == "__main__":
#     print(org_randint(6))

