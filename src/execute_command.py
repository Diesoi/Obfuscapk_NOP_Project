import os


def NOP(output_dir, working_dir, apk_path):
    cmd = "python -m obfuscapk.cli -o Nop -o Rebuild -o NewAlignment -d {0} -w {1} {2}".format(output_dir,
                                                                                               working_dir,
                                                                                               apk_path)
    os.system(cmd)


def EmptyFunction(output_dir, working_dir, apk_path):
    cmd = "python -m obfuscapk.cli -o EmptyFunction -o Rebuild -o NewAlignment -d {0} -w {1} {2}".format(output_dir,
                                                                                                         working_dir,
                                                                                                         apk_path)
    os.system(cmd)


def EmptyLoopFunction(output_dir, working_dir, apk_path):
    cmd = "python -m obfuscapk.cli -o EmptyLoopFunction -o Rebuild -o NewAlignment -d {0} -w {1} " \
          "{2}".format(output_dir,
                       working_dir,
                       apk_path)
    os.system(cmd)


def ExternalEmptyFunction(output_dir, working_dir, apk_path):
    cmd = "python -m obfuscapk.cli -o ExternalEmptyFunction -o Rebuild -o NewAlignment -d {0} -w {1} " \
          "{2}".format(output_dir,
                       working_dir,
                       apk_path)
    os.system(cmd)


def VoidFunction(output_dir, working_dir, apk_path):
    cmd = "python -m obfuscapk.cli -o VoidFunction -o Rebuild -o NewAlignment -d {0} -w {1} " \
          "{2}".format(output_dir,
                       working_dir,
                       apk_path)
    os.system(cmd)


if __name__ == "__main__":
    apk_path = 'C:\\Users\\diego\\Desktop\\NOP_Android\\Data\\test\\test1_original.apk'
    output_dir = 'C:\\Users\\diego\\Desktop\\NOP_Android\\Data\\test\\{0}_mod.apk'.format(apk_path.split('\\')[-1].split('.')[0].split('_')[0])
    working_dir = 'C:\\Users\\diego\\Desktop\\NOP_Android\\Data\\test\\word-dir'
    print(output_dir)
    ExternalEmptyFunction(output_dir, working_dir, apk_path)
