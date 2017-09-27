from static.statistical import distance_metrics


def compare(input1, input2):
    result = dict()
    for metric, func in distance_metrics.items():
        result[metric] = func(input1, input2)
#    print(result)
    result = {k: v for k, v in result.items() if not (v is None)}
#    print("Best:" + str({k: v for k, v in result.items() if v == max(result.values())}))
    return result
