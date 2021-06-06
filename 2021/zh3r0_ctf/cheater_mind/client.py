import pwn
import re


def do_guess(io, guess):
    s = " ".join(str(x) for x in guess)
    io.sendlineafter("enter your guess as space separated integers:\n", s)


def get_solver(N, K, mutation, guess_limit):
    cmd = f"timeout 45 mix run_genetic_algorithm {N} {K} {mutation} {guess_limit}"
    return pwn.process(cmd, cwd="./mastermind", shell=True)


def get_guess(solver):
    solver.recvuntil("I guess:\n")
    return eval(solver.recvlineS())


def get_results(io):
    s = io.recvlineS().strip()
    data = [int(x) for x in s.split()]

    correct_position = data[0]
    same_color = data[1] + correct_position

    s = io.recvlineS()
    if "level passed, good job" in s:
        return correct_position, same_color, True
    elif "You noob, try again" in s:
        raise ValueError("We lost")
    else:
        io.unrecv(s)
        return correct_position, same_color, False


def send_results(solver, correct_position, same_color):
    s = f"{correct_position} {same_color}"
    solver.sendlineafter("Enter move results:\n", s)


def get_game_params(io):
    s = io.recvlineS().strip()
    data = re.match(
        r"Level (\d+), N=(\d+), K=(\d+), mutation=(\d*\.?\d*), guess limit=(\d+)", s
    )
    level = int(data.group(1))
    N = int(data.group(2))
    K = int(data.group(3))
    mutation = float(data.group(4))
    guess_limit = int(data.group(5))
    return level, N, K, mutation, guess_limit


def play_level(io):
    level, N, K, mutation, guess_limit = get_game_params(io)
    pwn.log.info(
        "Level {}, N={}, K={}, mutation={}, guess limit={}".format(
            level, N, K, mutation, guess_limit
        )
    )

    solver = get_solver(N, K, mutation, guess_limit)
    for i in range(guess_limit):
        guess = get_guess(solver)
        do_guess(io, guess)
        correct_position, same_color, level_passed = get_results(io)
        if level_passed:
            pwn.log.info(f"Beat level {level}")
            break
        else:
            send_results(solver, correct_position, same_color)


def play():
    if pwn.args.REMOTE:
        io = pwn.remote("misc.zh3r0.cf", 1111)
    else:
        io = pwn.process("python3 challenge.py", shell=True)

    io.recvline()
    io.recvline()

    while True:
        play_level(io)
        s = io.recvlineS()
        if "you earned it" in s:
            open("flag.txt", "w").write(s)
            break
        else:
            io.unrecv(s)


pwn.context.log_level = "debug"

while True:
    try:
        play()
        break
    except Exception as e:
        print(e)
        continue
