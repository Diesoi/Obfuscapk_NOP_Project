import os
import random

def create_subset(data_dir):

    list_apks_subsamples = {'Benign': [],
                            'Malicious': []}
    for p in os.listdir(data_dir):
        dir = os.path.join(data_dir, p)
        for p1 in os.listdir(dir):
            list_apks_subsamples[p].append(p1.replace(".apk", ""))

    for p in os.listdir(data_dir):
        random.shuffle(list_apks_subsamples[p])

        file_path = os.path.join(data_dir, p + '.txt')
        with open(file_path, 'w') as fp:
            fp.write("\n".join(list_apks_subsamples[p][:500]))


def read_subset(data_dir):

    list_apk_subset = {'Benign': list(),
                       'Malicious': list()}

    for f in os.listdir(data_dir):
        if f.endswith(".txt"):
            file_path = os.path.join(data_dir, f)
            with open(file_path, 'r') as fp:
                list_apk_subset[f.replace(".txt", "")] = fp.read().split("\n")

    return list_apk_subset


if __name__ == '__main__':

    data_dir = os.path.join("..", "..", "Data", "Set")

    # create_subset(data_dir)
    list_apk_subset = read_subset(data_dir)
    print(list_apk_subset)
