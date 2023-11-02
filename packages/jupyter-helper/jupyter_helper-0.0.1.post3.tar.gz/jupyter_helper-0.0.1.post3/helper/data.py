#!/usr/bin/env python3

import bz2
import pickle


class Data:
    def __init__(self) -> None:
        pass

    @staticmethod
    def load_from(file):
        with bz2.BZ2File(file, "rb") as f:
            data = pickle.load(f)
            return data

    @staticmethod
    def save_to(data, file):
        with bz2.BZ2File(file, "wb") as f:
            pickle.dump(data, f)
