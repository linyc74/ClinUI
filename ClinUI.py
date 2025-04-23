from src import Main
from src.schema import NycuOsccSchema, VghtcOsccSchema, VghtpeHnsccSchema


if __name__ == '__main__':
    Main().main(schema=VghtcOsccSchema)
