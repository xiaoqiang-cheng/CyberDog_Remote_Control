


if __name__ == "__main__":

    import time
    @timeguard(timedelta(seconds=4),None)
    def add():
        print(12)

    for i in range(10):
        add()
        time.sleep(1)