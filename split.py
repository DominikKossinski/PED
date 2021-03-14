import pandas as pd


def split(file_name):
    df = pd.read_csv(file_name, index_col=0)
    print(df)
    n = len(df)
    h = n // 2
    t = n - h
    head = df.head(h)
    tail = df.tail(t)
    head.to_csv(file_name.replace(".csv", "_head.csv"))
    tail.to_csv(file_name.replace(".csv", "_tail.csv"))
    print(f"N: {n} K:{h} t:{t}")

def join(file_name):
    head = pd.read_csv(file_name.replace(".csv", "_head.csv"), index_col=0)
    tail = pd.read_csv(file_name.replace(".csv", "_tail.csv"), index_col=0)
    head = head.append(tail, ignore_index=True)
    print(head)

if __name__ == '__main__':
    split("description_words.csv")
    join("description_words.csv")
