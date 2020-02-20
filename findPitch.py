from statistics import mode

def findPitch(a):
    diffset =[]
    for i in range(len(a)-1):
        diffset.append(a[i+1] - a[i])

    return get_small_mode(diffset)



def get_small_mode(numbers):
    counts = {k:numbers.count(k) for k in set(numbers)}
    modes = sorted(dict(filter(lambda x: x[1] == max(counts.values()), counts.items())).keys())
    if len(modes) != 0:
        return modes[0]
    else:
        return mode(numbers)



