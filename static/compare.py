from static.phonetics import encPhoneVariants
from static.distances import compare


def full_compare(input1, input2):
    tmp = {}
    str1 = encPhoneVariants(input1)
    str2 = encPhoneVariants(input2)
    for key in set(str1.keys()).union(set(str2.keys())):
        tmp[key] = compare(str1.get(key, ""), str2.get(key, ""))
    result = {}
    for k1, v1 in tmp.items():
        for k2, v2 in v1.items():
            result[k2 + ": " + k1] = v2
    return result


def mult_full_compare(l1):
    combinations=list(zip(l1, l1[1:]))
    tmp = list(map(lambda x:full_compare(x[0],x[1]), combinations))
    result={}
    for key in tmp[0].keys():
        result[key]=list(map(lambda x: x[key],tmp))
    return result
