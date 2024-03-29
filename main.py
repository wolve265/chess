import sys

sys.path.insert(0, "src")
from chess import Chess  # noqa: E402

if __name__ == "__main__":
    if sys.version_info < (3, 10):
        print("This chess app requires Python 3.10 or newer.")
        sys.exit(1)
    chess = Chess()
    chess.run()
