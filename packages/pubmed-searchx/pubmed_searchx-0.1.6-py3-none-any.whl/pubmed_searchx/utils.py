import time
import os


def getCurrentTimeString(no_space=True):
    t = time.localtime()
    currentTime = time.strftime("%Y-%m-%d %H:%M:%S", t)
    currentTime = currentTime.replace(":", "_").replace("-", "_")

    if no_space:
        currentTime = currentTime.replace(" ", "_")
    return currentTime


def load_list_from_file(path):
    fin = open(path)
    ls = []
    while True:
        line = fin.readline()
        if line == "":
            break
        ls.append(line.strip())
    fin.close()
    return ls


def ensureDir(path):
    if not os.path.exists(path):
        os.makedirs(path)


def print_db(flag, *args):
    if flag:
        print(*args)


if __name__ == "__main__":
    print_db(True, "A", "B", "C")
