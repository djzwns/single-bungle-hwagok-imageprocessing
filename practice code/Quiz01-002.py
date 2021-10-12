# function

# global var
ary = []
total = 0

# main
for i in range(12345, 67891, 1):
    if i % 3128 == 0:
        ary.append(i)

for i in range(len(ary)):
    total += ary[i]

print(ary)
print(total)
