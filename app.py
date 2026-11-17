from app.app_manager import AppManager
from main import main


def run():

    app = AppManager()

    app.start()

    try:

        main()

    finally:

        app.stop()


if __name__ == "__main__":

    run()