import statistics


def analyse_single(data):
    result = {}
    result["best match"] = max(data.values())
    result["best match algorithms"] = [k for k, v in data.items() if v == result["best match"]]
    result["worst match"] = min(data.values())
    result["worst match algorithms"] = [k for k, v in data.items() if v == result["worst match"]]
    result["avarage match"] = statistics.mean(data.values())
    result["median match"] = statistics.mean(data.values())
    return result

def analyse_mult(data):
    result = {}
    return result