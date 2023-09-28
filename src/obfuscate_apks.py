import execute_command
from select_subsamples import read_subset
import os


if __name__ == '__main__':

    data_dir = os.path.join(" ", "disks", "raid10T", "DataNOP", "Set").strip()
    list_apk = read_subset(data_dir)

    for k in list_apk:
        sample_path = os.path.join(data_dir, k)
        for apk in os.listdir(sample_path):
            if apk.replace(".apk", "") in list_apk[k] and \
                    apk not in os.listdir(os.path.join(sample_path, "Obfuscated")):
                apk_path = os.path.join(sample_path, apk)
                working_dir = os.path.join(sample_path, "work-dir")
                output_dir = os.path.join(sample_path, "Obfuscated", apk)
                execute_command.CombineAll(output_dir=output_dir,
                                           apk_path=apk_path)

