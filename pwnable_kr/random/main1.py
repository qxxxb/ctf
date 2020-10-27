from subprocess import Popen, PIPE

for i in range(2 ** 4):
    p = Popen(['./random'], stdout=PIPE, stdin=PIPE, stderr=PIPE)
    response = p.communicate(input=i)[0].decode(errors='replace')
    print(response)
    if response[:5] != "Wrong":
        break
