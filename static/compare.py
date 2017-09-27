from static.phonetics import encPhoneVariants
from static.distances import compare


def full_compare(input1, input2):
    tmp = {}
    str1 = encPhoneVariants(input1)
    str2 = encPhoneVariants(input2)
    for key in str1.keys():
        tmp[key] = compare(str1[key], str2[key])
    result={}
    for k1,v1 in tmp.items():
        for k2,v2 in v1.items():
            result[k2+": "+k1]=v2
    return result
