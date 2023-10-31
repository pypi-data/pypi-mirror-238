import math
import hashlib

def trailing_zeros(hash_value):
    count = 0
    while (hash_value & 1) == 0:
        count += 1
        hash_value >>= 1
    return count

def fm_algorithm(stream, hash_functions):
    max_trailing_zeros = 0

    for item in stream:
        for i in range(hash_functions):
            hash_object = hashlib.sha256()
            hash_object.update(str(item).encode())
            hash_object.update(str(i).encode())
            hash_value = int(hash_object.hexdigest(), 16)
            max_trailing_zeros = max(max_trailing_zeros, trailing_zeros(hash_value))

    return 2 ** max_trailing_zeros

stream = [1, 2, 3, 4, 1, 2, 5, 6, 7, 8]

# Number of hash functions to use
hash_functions = 6

estimated_distinct_count = fm_algorithm(stream, hash_functions)
print("Estimated distinct count:", estimated_distinct_count)

def trail(n):
    bits = 0
    x = n

    if x:
        while (x & 1) == 0:
            bits += 1
            x >>= 1
    return bits

def decToBinary(n):
    binaryNum = [0] * 32
    i = 0
    while n > 0:
        binaryNum[i] = n % 2
        n = n // 2
        i += 1

    ans = ""
    for j in range(i - 1, -1, -1):
        ans += str(binaryNum[j])
    return ans

def main():
    n = int(input())
    a = []
    bin = []
    mx = 0

    for _ in range(n):
        a_i = int(input())
        qs = (6 * a_i + 1) % 5
        ans = decToBinary(a_i)
        bin.append(ans)

    for i in range(len(bin)):
        j = int(bin[i], 2)
        maxi = trail(j)
        mx = max(mx, maxi)

    print(2**mx)


main()