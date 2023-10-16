import execute_command
from select_subsamples import read_subset
import os


if __name__ == '__main__':

    data_dir = os.path.join("..", "..", "Data", "Set")
    list_apk = read_subset(data_dir)

    for k in list_apk:
        sample_path = os.path.join(data_dir, k)
        for apk in os.listdir(sample_path):
            if apk.replace(".apk", "") not in list_apk[k] and \
                    apk not in os.listdir(os.path.join(sample_path, "Obfuscated")):
                apk_path = os.path.join(sample_path, apk)
                print(apk_path)
                working_dir = os.path.join(sample_path, "work-dir")
                output_dir = os.path.join(sample_path, "Obfuscated", apk)
                execute_command.EmptyFunction(output_dir=output_dir,
                                              working_dir=working_dir,
                                              apk_path=apk_path)
            break
        break
