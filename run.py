from src.utils import initialize_databases
from src.ui import create_ui


def run():
    # Initialize the databases
    initialize_databases()

    # Create the user interface
    create_ui()


if __name__ == "__main__":
    run()
