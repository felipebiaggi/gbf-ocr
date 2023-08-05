import multiprocessing
import threading


def start_bot():
    print(f"foo: <{multiprocessing.current_process()}>")


if __name__ == "__main__":
    print(f"main: <{threading.get_ident()}>")

    bot_process = multiprocessing.Process(target=start_bot)

    bot_process.start()
    bot_process.is_alive()