import os
from obfuscapk.tool import Apktool
from obfuscapk.obfuscation import Obfuscation
import random
import glob
from obfuscapk.util import inplace_edit_file

def print_definitions(definitions):

    for defin in definitions:
        for line in defin.split("\n"):
            print(line)


def find_smali(output_dir):
    smali_files = []
    smali_file_pattern = os.path.join(output_dir, '**/*.smali')
    smali_files = glob.glob(smali_file_pattern, recursive=True)
    definitions = []
    for smali_file in smali_files:
        # print(smali_file)
        # smali_files.append(smali_file)
        method_definition = ""
        previous = ""
        direct_methods = False
        with inplace_edit_file(smali_file) as (in_file, out_file):
            for line in in_file:
                print(line)
                if '.end method' in line:
                    method_definition += line
                    definitions.append(method_definition)
                    method_definition = ""
                elif '# direct methods' in line or '# virtual methods' in line:
                    direct_methods = True
                elif ".method" in line and "constructor" not in line and direct_methods:
                    # print(line)
                    method_definition += line
                    previous = line
                elif ".method" in previous and "constructor" not in previous:
                    method_definition += line
        break

    print("Definitions: ")
    print_definitions(definitions)

    return smali_files


def main(path_to_apks, output_dir):
    
    apks_to_decompile = [apk for apk in os.listdir(path_to_apks)]
    random.shuffle(apks_to_decompile)
    apks_to_decompile = apks_to_decompile[:50]
    apktool = Apktool()
    
    for apk in apks_to_decompile:
        input_path = os.path.join(path_to_apks, apk)
        output_path = os.path.join(output_dir, apk.replace('.apk', ''))
        apktool.decode(input_path, output_path, True)

        smali_files = find_smali(output_path)
        
        break



if __name__ == '__main__':


    path_to_apks = os.path.join("/mnt", "NasNOP", "Set", "Benign", "Benign_original")
    output_dir = os.path.join("/mnt", "NasNOP", "Set", "Benign", "tmpdir")
    main(path_to_apks, output_dir)