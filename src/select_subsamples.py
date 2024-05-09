import os
import random
import json


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


def add_samples(data_dir):

    list_apk_subset = read_subset(data_dir)

    added = {'Benign': list(),
             'Malicious': list()}

    for t in list_apk_subset.keys():
        for apk in os.listdir(os.join(data_dir, t)):
            if apk.replace(".apk", "") not in list_apk_subset[t]:
                added[t].append(apk.replace(".apk", ""))
    
    for t in list_apk_subset.keys():
        random.shuffle(added[t])

        file_path = os.path.join(data_dir, t + '.txt')
        with open(file_path, 'a') as fp:
            fp.write("\n".join(added[t][:502]))


def select_year(data_dir):

    list_apk_subset = read_subset(data_dir)
    with open(os.path.join(data_dir, "Benign.json")) as fp:
        benign_year = json.load(fp)
    with open(os.path.join(data_dir, "Malicious.json")) as fp:
        malicious_year = json.load(fp)

    # print(benign_year, malicious_year)
    counter = {str(k): 0 for k in range(2008, 2023)}

    i = 1
    """
    for type in list_apk_subset.keys():
        for apk in list_apk_subset[type]:
            print(i)
            try:
                if type == 'Benign':
                    counter[benign_year[apk]] += 1
                else:
                    counter[malicious_year[apk]] += 1
                i += 1
            except:
                pass
    """

    for type in list_apk_subset.keys():
        for apk in os.listdir(os.path.join(data_dir, type)):
            try:
                if type == 'Benign':
                    counter[benign_year[apk.replace(".apk", "")]] += 1
                else:
                    counter[malicious_year[apk.replace(".apk", "")]] += 1
            except:
                pass
    print(counter)
    
def add_samples(data_dir):

    list_apk_subset = read_subset(data_dir)

    added = {'Benign': list(),
             'Malicious': list()}

    for t in list_apk_subset.keys():
        for apk in os.listdir(os.path.join(data_dir, t)):
            if apk.replace(".apk", "") not in list_apk_subset[t]:
                added[t].append(apk.replace(".apk", ""))
    
    for t in list_apk_subset.keys():
        random.shuffle(added[t])

        file_path = os.path.join(data_dir, t + '.txt')
        with open(file_path, 'a') as fp:
            fp.write("\n".join(added[t][:502])) 


if __name__ == '__main__':

    data_dir = os.path.join("..", "..", "Data", "Set")
    # data_dir = os.path.join(" ", "disks", "raid10T", "DataNOP", "Set").strip()

    # create_subset(data_dir)
    # list_apk_subset = read_subset(data_dir)
    # select_year(data_dir)
    
    add_samples(data_dir)
    
    
    
    
    
    
    
