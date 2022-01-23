#!/usr/bin/env python
import engine
import data_manager


def main():
    data_manager.start()
    try:
        engine.start()
    finally:
        data_manager.stop()


main()
