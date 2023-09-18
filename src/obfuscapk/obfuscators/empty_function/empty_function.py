import logging
import random
import string

from obfuscapk import obfuscator_category
from obfuscapk import util
from obfuscapk.obfuscation import Obfuscation


class EmptyFunction(obfuscator_category.ICodeObfuscator):

    def __init__(self):
        self.logger = logging.getLogger(
            "{0}.{1}".format(__name__, self.__class__.__name__)
        )
        super().__init__()

    def add_empty_function(self, smali_file):

        # empty method definition
        function_name = util.generate_random_name()
        function_definition = (
            ".method public static {0}()V\n"
            "\t.registers 0\n"
            "\t.line 1\n"
            "\t.prologue\n"
            "\t# The function does nothing\n"
            "\treturn-void\n"
            ".end method\n"
        ).format(function_name)

        with util.inplace_edit_file(smali_file) as (input_file, output_file):
            # inserting the static method inside the smali file after # direct methods comment
            for line in input_file:
                if "# direct methods" in line:
                    output_file.write(line)
                    output_file.write(function_definition)
                else:
                    output_file.write(line)

        return function_name

    def add_call_to_emtpy(self, smali_file):
        self.logger.debug(
            'Inserting call to empty function in file "{0}"'.format(smali_file))
        function_name = self.add_empty_function(smali_file)

        with util.inplace_edit_file(smali_file) as (input_file, output_file):
            for line in input_file:
                # if a function call is found (invoke-* opcode)
                # the call to empty_function() is injected before the real call
                invoke_match = util.invoke_pattern.match(line)
                if invoke_match:
                    # randomizing invocation 
                    if random.choice([True, False]):
                        output_file.write("\tinvoke-static {{}}, {0}()V\n".format(function_name))
                        output_file.write(line)
                    else:
                        output_file.write(line)
                # otherwise the original smali line is written
                else:
                    output_file.write(line)

    def treat_dex(self, smali_files, max_methods_to_add, interactive):
        # treat single dex to check the limit to calls
        added_methods = 0
        for smali_file in util.show_list_progress(
                smali_files,
                interactive=interactive,
                description="Inserting call to empty function in smali files"):
            if added_methods < max_methods_to_add:
                self.add_call_to_emtpy(smali_file)
                added_methods += 1
            else:
                break

    def obfuscate(self, obfuscation_info: Obfuscation):
        self.logger.info('Running "{0}" obfuscator'.format(self.__class__.__name__))

        try:
            # there is a method call limit for dex files
            max_methods_to_add = obfuscation_info.get_remaining_methods_per_obfuscator()

            if obfuscation_info.is_multidex():
                for index, dex_smali_files in enumerate(util.show_list_progress(
                        obfuscation_info.get_multidex_smali_files(),
                        interactive=obfuscation_info.interactive,
                        unit="dex",
                        description="Processing multidex")):
                    max_methods_to_add = (obfuscation_info.get_remaining_methods_per_obfuscator()[index])
                    self.treat_dex(dex_smali_files, max_methods_to_add, obfuscation_info.interactive)
            else:
                self.treat_dex(obfuscation_info.get_smali_files(), max_methods_to_add, obfuscation_info.interactive)
        except Exception as e:
            self.logger.error(
                'Error during execution of "{0}" obfuscator: {1}'.format(
                    self.__class__.__name__, e
                )
            )
            raise

        finally:
            obfuscation_info.used_obfuscators.append(self.__class__.__name__)
