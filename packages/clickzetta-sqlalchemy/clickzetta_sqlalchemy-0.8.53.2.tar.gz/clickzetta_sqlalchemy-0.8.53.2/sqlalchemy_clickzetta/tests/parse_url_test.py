import io
from contextlib import closing

import sqlalchemy
from sqlalchemy.engine.url import make_url
from sqlalchemy import create_engine
import pytest
import csv


def test_csv():
    test = "ansm,nihao,women\\,haoya,sanmefem"
    csv.register_dialect('cz_dialect', delimiter=',', escapechar='\\')
    reader = csv.reader(io.StringIO(test), dialect='cz_dialect')
    for line in reader:
        for i in range(len(line)):
            print(line[i])