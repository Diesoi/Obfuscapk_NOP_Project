import os

def NOP(output_dir, working_dir, apk_path):
    cmd = "python -m obfuscapk.cli -o Nop -o Rebuild -o NewAlignment -d {0} -w {1} {2}".format(output_dir,
                                                                                               working_dir,
                                                                                               apk_path)
    os.system(cmd)


if __name__ == "__main__":

    apk_path = 'C:\\Users\\diego\\Desktop\\NOP_Android\\Data\\phoneword_original.apk'
    output_dir = 'C:\\Users\\diego\\Desktop\\{0}.apk'.format(apk_path.split('\\')[-1].split('.')[0])
    working_dir = 'C:\\Users\\diego\\Desktop\\NOP_Android\\Data\\word-dir'
    print(output_dir)
    NOP(output_dir, working_dir, apk_path)
