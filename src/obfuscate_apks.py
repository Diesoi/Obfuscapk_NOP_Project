import execute_command
from select_subsamples import read_subset
import os
import argparse
import subprocess
import shutil
import sys


def get_cmd_args(args):
    """
    Parse and return the command line parameters needed for the script execution.

    :param args: List of arguments to be parsed (by default sys.argv is used).
    :return: The command line needed parameters.
    """

    parser = argparse.ArgumentParser()

    parser.add_argument(
        "-o"
        "--obfuscator",
        type=str,
        help="One of proposed obfuscators - EmptyFunction, EmptyLoopFunction, EmptyLoopMeanFunction, ExternalEmptyFunction, VoidFunction, CombineAll"
    )

    return parser.parse_args(args)


if __name__ == '__main__':

    # data_dir = os.path.join(" ", "disks", "raid10T", "DataNOP", "Set").strip()
    data_dir = os.path.join(" ", "mnt", "NasNOP", "Set", "Malcious", 'Malicious_original').strip()
    # list_apk = read_subset(data_dir)

    #args = get_cmd_args()

    mal_path = os.path.join('/mnt', 'NasNOP', 'Set', 'Malicious', 'Evasion', 'Malware')
    # with open('../../Deep-Android-Malware-Detection/droidbot.txt', 'r') as fp:
    #    list_apk = fp.readlines()
    list_apk = os.listdir(mal_path)

    # print(list_apk)
    with open('droidbot.txt', 'r') as f:
        list_apk = f.read().split('\n')

    for i, apk in enumerate(list_apk):

        """apk_path = os.path.join(mal_path, apk.replace('\n', ''))
        print(apk_path)
        output_dir = os.path.join(mal_path, apk.replace('\n', ''))
        execute_command.rebuild(output_dir=output_dir, working_dir='/mnt/NasNOP/Set/Malicious/tmpdir/', 
                                apk_path=apk_path)
        tmp_folder = '/mnt/NasNOP/Set/Malicious/tmpdir/' + apk_path.split("/")[-1].replace(".apk", "")
        shutil.rmtree(tmp_folder, ignore_errors=True)"""

        if apk in os.listdir(os.path.join('/mnt', 'NasNOP', 'Set/Malicious/NOP')):
            continue

        apk_path = os.path.join(mal_path, apk)
        print(apk_path)
        output_dir = os.path.join('/mnt', 'NasNOP', 'Set/Malicious/NOP', apk)
        execute_command.NOP(output_dir=output_dir, working_dir='/mnt/NasNOP/Set/Malicious/tmpdir/', apk_path=apk_path)
        tmp_folder = '/mnt/NasNOP/Set/Malicious/tmpdir/' + apk_path.split("/")[-1].replace(".apk", "")
        shutil.rmtree(tmp_folder, ignore_errors=True)


    """for k in list_apk:
        dir_path = os.path.join(data_dir, k)
        sample_path = os.path.join(dir_path, k+"_original")
        print(sample_path)
        print(len(os.listdir(sample_path)))
        i = 0
        for apk in os.listdir(sample_path):
            if apk.replace(".apk", "") not in list_apk[k] and i<100:
                apk_path = os.path.join(sample_path, apk)
                print(apk_path)
                output_dir = os.path.join(dir_path, "OpcodeInj3", apk)
                execute_command.NOP(output_dir=output_dir,
                                          working_dir='/tmp/',
                                          apk_path=apk_path)
                tmp_folder = '/tmp/' + apk_path.split("/")[-1].replace(".apk", "")
                shutil.rmtree(tmp_folder, ignore_errors=True)
                i+=1
        print(k, i)"""
