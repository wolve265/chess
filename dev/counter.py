import glob


if __name__ == "__main__":
    counter = 0

    files = glob.glob("**/*.py", recursive=True)
    for file in files:
        with open(file, "r") as fh:
            counter += len(fh.readlines())

    print(counter)
