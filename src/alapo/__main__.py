from alapo.app import Alapo
from alapo.app.meta.Process import Process


def main() -> None:
    app: Process = Alapo()
    app.start()


if __name__ == "__main__":
    main()
