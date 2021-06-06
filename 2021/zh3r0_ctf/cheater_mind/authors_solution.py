from z3 import Int, Solver, And, Or, sat, If, Sum, Optimize
from collections import Counter
import pwn
REM = pwn.process('python3 challenge.py',shell=True)
#REM = pwn.remote('2.tcp.ngrok.io',12456)
data = REM.recvuntil(b'integers:')
level_regex = b'.*N=(\d+), K=(\d+), mutation=(.*), guess limit=(\d+)'
m = pwn.re.search(level_regex,data).groups()


#Level 1, N=6, K=6, mutation=0, guess limit=6

class Solver:
    def __init__(self,N,K,REM):
        self.N=N
        self.K=K
        self.board = [Int(str(i)) for i in range(K)]
        self.solver = Optimize()
        self.solver.add([And(self.board[i] <= N, self.board[i] >= 1)
                         for i in range(K)])

    def agent(self,query):
        REM.sendline(' '.join(map(str,query)))
        data = REM.recvuntil(b'integers:')
        a,b = pwn.re.search(b'(\d+) (\d+)\n',data).groups()
        m = pwn.re.search(level_regex,data)
        if m:
            return int(a),int(b),m.groups()
        return int(a),int(b)

    def next(self):
        if self.solver.check()==sat:
            model = self.solver.model()
            query = [model[self.board[i]].as_long() for i in range(self.K)]
        print(query)
        minvals = []
        for val in range(1, self.N+1):
            count_board = Sum([If((self.board[i] == val), 1, 0)
                               for i in range(self.K)])
            count_query = Sum([If((query[i] == val), 1, 0)
                               for i in range(self.K)])
            minvals.append(If(count_board < count_query,
                              count_board, count_query))
        agent_resp = self.agent(query)
        bulls, cows = agent_resp[:2]
        print(bulls,cows)
        if bulls == self.K:
            # If all predicted correctly
            N,K,mut,lim = agent_resp[2]
            print(N,K,mut,lim)
            self.__init__(int(N),int(K),REM)
            return True
        exactly_equal = Sum([If(self.board[i] == query[i], 1, 0)
                             for i in range(self.K)])
        self.solver.add_soft(exactly_equal == bulls)
        self.solver.add_soft(Sum(minvals) == bulls+cows)
        # Not predicted correctly yet
        return False


s = Solver(int(m[0]),int(m[1]),REM)
while True:
    s.next()
