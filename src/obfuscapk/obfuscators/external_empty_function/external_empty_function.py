import logging
import re
import random
import os

from obfuscapk import obfuscator_category
from obfuscapk import util
from obfuscapk.obfuscation import Obfuscation


class ExternalEmptyFunction(obfuscator_category.ICodeObfuscator):

    def __init__(self):
        self.logger = logging.getLogger(
            "{0}.{1}".format(__name__, self.__class__.__name__)
        )
        super().__init__()

    def add_external_class(self, obfuscation_info, max_methods_to_add, path_to_smali_folder):

        # class_name = "LMyClass/ExternalEmpty"
        dir_name = util.generate_random_name()
        class_name = util.generate_random_name()
        class_in_smali = "L" + dir_name + '/' + class_name
        function_name = util.generate_random_name()
        class_definition = (
            ".class public {0};\n"
            ".super Ljava/lang/Object;\n\n"
            ".method public constructor <init>()V"
            "\t.registers 1\n"
            "\tinvoke-direct {{p0}}, Ljava/lang/Object;-><init>()V\n"
            "\treturn-void\n"
            ".end method\n"
            "\n"
            ".method public static {1}()V\n"
            "\t.registers 0\n"
            "\t.line 1\n"
            "\t.prologue\n"
            "\t# The function does nothing\n"
            "\treturn-void\n"
            ".end method"
        ).format(class_in_smali, function_name)

        added_methods = 0
        if added_methods < max_methods_to_add:
            pattern = re.compile(r"\\(smali[0-9a-zA-Z_]*\\)")

            match = re.search(pattern, path_to_smali_folder)
            split = match.group(1)
            smali_dir = os.path.join(path_to_smali_folder.split(split)[0], split, dir_name)

            # print("Smali: ", smali_dir)
            os.mkdir(smali_dir)
            path_to_new_smali = os.path.join(smali_dir, "{0}.smali".format(class_name))

            with open(path_to_new_smali, "w") as file:
                file.write(class_definition)
            return path_to_new_smali, True, function_name
        else:
            return None, False

    def add_call(self, smali_files, smali_to_call, interactive, function_name):

        for smali_file in util.show_list_progress(
                smali_files,
                interactive=interactive,
                description="Inserting call to MyClass empty function in smali files"):
            self.logger.debug(
                'Inserting call to empty function in file "{0}"'.format(smali_file))

            class_name = "L" + "\\".join(smali_to_call.rsplit("\\", 2)[-2:]).replace(".smali", "").replace("\\", "/")
            print(class_name)
            print(function_name)
            with util.inplace_edit_file(smali_file) as (input_file, output_file):
                for line in input_file:
                    invoke_match = util.invoke_pattern.match(line)
                    if random.choice([True, False]):
                        if invoke_match:
                            output_file.write("\tinvoke-static {{}}, {0};->{1}()V\n".format(class_name, function_name))
                            output_file.write(line)
                        else:
                            output_file.write(line)
                    # otherwise the original smali line is written
                    else:
                        output_file.write(line)

    def obfuscate(self, obfuscation_info: Obfuscation):
        self.logger.info('Running "{0}" obfuscator'.format(self.__class__.__name__))

        try:
            max_methods_to_add = obfuscation_info.get_remaining_methods_per_obfuscator()

            if obfuscation_info.is_multidex():
                for index, dex_smali_files in enumerate(util.show_list_progress(
                        obfuscation_info.get_multidex_smali_files(),
                        interactive=obfuscation_info.interactive,
                        unit="dex",
                        description="Processing multidex")):
                    added_class = False
                    path_to_smali = None
                    max_methods_to_add = obfuscation_info.get_remaining_methods_per_obfuscator()[index]
                    if not added_class:
                        path_to_smali, added_class, function_name = self.add_external_class(obfuscation_info, max_methods_to_add,
                                                                             dex_smali_files[0])
                        print("F_name ", function_name)

                    self.add_call(dex_smali_files, path_to_smali, obfuscation_info.interactive,
                                  function_name)
            else:
                path_to_smali, added_class, function_name = self.add_external_class(obfuscation_info, max_methods_to_add,
                                                                     obfuscation_info.get_smali_files()[0])

                print("F_name ", function_name)
                self.add_call(obfuscation_info.get_smali_files(), path_to_smali, obfuscation_info.interactive,
                              function_name)
        except Exception as e:
            self.logger.error(
                'Error during execution of "{0}" obfuscator: {1}'.format(
                    self.__class__.__name__, e
                )
            )
            raise

        finally:
            obfuscation_info.used_obfuscators.append(self.__class__.__name__)



"""import logging
import re
import random
import os

from obfuscapk import obfuscator_category
from obfuscapk import util
from obfuscapk.obfuscation import Obfuscation


class ExternalEmptyFunction(obfuscator_category.ICodeObfuscator):

    def __init__(self):
        self.logger = logging.getLogger(
            "{0}.{1}".format(__name__, self.__class__.__name__)
        )
        super().__init__()

    def add_external_class(self, obfuscation_info, max_methods_to_add, path_to_smali_folder):

        class_name = "ExternalEmpty"
        function_name = "EmptyFunction"
        class_definition = (
            ".class public {0};\n"
            ".super Ljava/lang/Object;\n\n"
            ".method public constructor <init>()V"
            "\t.registers 1\n"
            "\tinvoke-direct {{p0}}, Ljava/lang/Object;-><init>()V\n"
            "\treturn-void\n"
            ".end method\n"
            "\n"
            ".method public static {1}()V\n"
            "\t.registers 0\n"
            "\t.line 1\n"
            "\t.prologue\n"
            "\t# The function does nothing\n"
            "\treturn-void\n"
            ".end method"
        ).format(class_name, function_name)

        added_methods = 0
        if added_methods < max_methods_to_add:
            pattern = re.compile(r"\\(smali[0-9a-zA-Z_]*\\)")

            match = re.search(pattern, path_to_smali_folder)
            split = match.group(1)
            smali_dir = os.path.join(path_to_smali_folder.split(split)[0], split, "MyClass")

            # print("Smali: ", smali_dir)
            os.mkdir(smali_dir)
            path_to_new_smali = os.path.join(smali_dir, "{0}.smali".format(class_name))

            with open(path_to_new_smali, "w") as file:
                file.write(class_definition)

            return path_to_new_smali, True
        else:
            return None, False

    def add_call(self, smali_files, smali_to_call, interactive):

        for smali_file in util.show_list_progress(
                smali_files,
                interactive=interactive,
                description="Inserting call to MyClass empty function in smali files"):
            self.logger.debug(
                'Inserting call to empty function in file "{0}"'.format(smali_file))

            class_name = "L" + "\\".join(smali_to_call.rsplit("\\", 2)[-2:]).replace(".smali", "").replace("\\", "/")
            with util.inplace_edit_file(smali_file) as (input_file, output_file):
                for line in input_file:
                    invoke_match = util.invoke_pattern.match(line)
                    if random.choice([True, False]):
                        if invoke_match:
                            output_file.write("\tinvoke-static {{}}, {0};->EmptyFunction()V\n".format(class_name))
                            output_file.write(line)
                        else:
                            output_file.write(line)
                    # otherwise the original smali line is written
                    else:
                        output_file.write(line)

    def obfuscate(self, obfuscation_info: Obfuscation):
        self.logger.info('Running "{0}" obfuscator'.format(self.__class__.__name__))

        try:
            max_methods_to_add = obfuscation_info.get_remaining_methods_per_obfuscator()

            if obfuscation_info.is_multidex():
                for index, dex_smali_files in enumerate(util.show_list_progress(
                        obfuscation_info.get_multidex_smali_files(),
                        interactive=obfuscation_info.interactive,
                        unit="dex",
                        description="Processing multidex")):
                    added_class = False
                    path_to_smali = None
                    max_methods_to_add = obfuscation_info.get_remaining_methods_per_obfuscator()[index]
                    if not added_class:
                        path_to_smali, added_class = self.add_external_class(obfuscation_info, max_methods_to_add,
                                                                             dex_smali_files[0])
                    # self.treat_dex(dex_smali_files, max_methods_to_add, obfuscation_info, path_to_smali)
                    self.add_call(dex_smali_files, path_to_smali, obfuscation_info.interactive)
            else:
                path_to_smali, added_class = self.add_external_class(obfuscation_info, max_methods_to_add,
                                                                     obfuscation_info.get_smali_files()[0])
                # self.treat_dex(obfuscation_info.get_smali_files(), max_methods_to_add,
                #               obfuscation_info, path_to_smali)
                self.add_call(obfuscation_info.get_smali_files(), path_to_smali, obfuscation_info.interactive)
        except Exception as e:
            self.logger.error(
                'Error during execution of "{0}" obfuscator: {1}'.format(
                    self.__class__.__name__, e
                )
            )
            raise

        finally:
            obfuscation_info.used_obfuscators.append(self.__class__.__name__)"""
