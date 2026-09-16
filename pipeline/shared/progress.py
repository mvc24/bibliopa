from time import sleep

from annotated_types import T


def progress(current, total, width=50):

    percent = (current / total) * 100 if total > 0 else 0

    left = width * percent // 100
    right = width - left
    print(f"\r[{'∞' * int(left)}{' ' * int(right)}] {percent:.2f}% done", end="", flush=True)
    sleep(0.1)
    # print("[", "∞" * left, " " * right, "]", f" {percent:.2f}", flush=True)
