from itertools import groupby

def look_and_say(iterations, sequence='1'):
    arr = [sequence]
    def get_sequence(arr,iterations,sequence):
        if iterations == 0:
            return arr
        else:
            current = ''.join(str(len(list(group))) + key for key,group in groupby(sequence))
            arr.append(current)
            get_sequence(arr,iterations-1,current)
        return arr
    
    final_sequence = get_sequence(arr,iterations,sequence)
    return final_sequence