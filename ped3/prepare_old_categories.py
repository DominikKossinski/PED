import os

import numpy as np
import pandas as pd
from numpy import nan

from helpers.files import get_csv_files


def get_float_or_nan(x):
    x = np.array(x)
    not_nans = list(x[np.logical_not(np.isnan(x))])
    if len(not_nans) == 0:
        return nan
    elif len(not_nans) == 1:
        return not_nans[0]
    else:
        return not_nans[-1]


def main():
    data_path = os.path.join("..", "categories_data")
    names = get_csv_files(data_path)
    for name in names:
        print(name)
        df = pd.read_csv(os.path.join(data_path, name), sep=";", index_col=0)
        old_categories = []
        for i in range(len(df)):
            row = df.iloc[i]
            new_cat = get_float_or_nan(eval(row["category_id"]))
            old_categories.append(new_cat)
        df["category_id"] = old_categories
        df.to_csv(os.path.join(data_path, name), sep=";")
        # df["category_id"] = df["category_id"].apply(lambda x: get_float_or_nan(eval(x)))


if __name__ == '__main__':
    main()
