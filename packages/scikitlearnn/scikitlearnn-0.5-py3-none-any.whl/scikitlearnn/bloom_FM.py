# **************************************** BLOOM ***********************************************************

m = int(input('enter mod: '))
n = int(input('enter number of hash functions: '))

hashes = []
for i in range(0, n):
	fxn = input(f'enter hash fxn {i+1}: ')
	hash = []
	for j in range(0, len(fxn)):
		if fxn[j] == 'x':
			if j == 0:
				hash.append(1)
			else:
				hash.append(int(fxn[j-1]))
		elif fxn[j] == '+':
			hash.append(int(fxn[j+1]))
	
	if len(hash) == 1:
		hash.append(0)
	hashes.append(hash)

filter = [0 for i in range(0, m)]
print(f'\ncurrent bloom filter: {filter}')

n = int(input('\nenter number of values to insert: '))
for i in range(0, n):
	v = int(input(f'enter value {i+1}: '))
	for hash in hashes:
		filter[(v*hash[0]+hash[1])%m] = 1
	print(f'current bloom filter: {filter}\n')


n = int(input('\nenter number of values to query: '))
for i in range(0, n):
	v = int(input(f'enter value {i+1}: '))
	neg = False
	for hash in hashes:
		if filter[(v*hash[0]+hash[1])%m] == 0:
			print(f'{v} is surely not present - NEGATIVE\n')
			neg = True
			break

	if neg == False:
		print(f'{v} is probably present - FALSE POSITIVE\n')

        

	

# ************************************************** FM *************************************************

items=[1,2,3,4,1,3,4,1,2,4,1,2,3]

def hash(x):
    x=(6*x)+1
    return x%5

def binary(x):
    return bin(x)[2:]

hashed=list(map(hash,items))
binaries=list(map(binary,hashed))

def count_0s(x):
    final_out,temp_out = 0,0
    out=False
    
    for ch in x[::-1]:
        if ch=='1':
            out=True
            break
        
        temp_out+=1
        
    if out:
        final_out=temp_out
    return final_out
        
counts=list(map(count_0s,binaries))
print("number of uniques:",2**max(counts))
