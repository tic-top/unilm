# https://pypi.org/project/python-Levenshtein/
# pip install python-Levenshtein
from Levenshtein import distance

def calculate_ned(str1, str2):

    if len(str1) == 0 and len(str2) == 0:
        d = 0
        ned = 1
        return d, ned

    d = distance(str1, str2)
    ned = 1 - d / max(len(str1), len(str2))
    return ned


# test
if __name__ == '__main__':

    testcases = [
        ['123', '456'],
        ['123', '123'],
        ['133', '123'],
        ['', ''],
        ['0123', '']
    ]

    total = 0
    sum = 0
    for testcase in testcases:
        str1, str2 = testcase
        d, ned = calculate_ned(str1, str2)       
        print(f'{str1} {str2} ned: {ned}, d: {d}')
        total += 1 
        sum += ned

    print('ned score: ', sum / total)