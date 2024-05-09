import logging
import random
import re
import string
import os

from obfuscapk import obfuscator_category
from obfuscapk import util
from obfuscapk.obfuscation import Obfuscation


class OpcodeInjection(obfuscator_category.ICodeObfuscator):

    def __init__(self):
        self.logger = logging.getLogger(
            "{0}.{1}".format(__name__, self.__class__.__name__)
        )
        super().__init__()

    @staticmethod
    def get_opcode_list():
        to_return = list()
        # print(os.listdir(os.getcwd()))
        with open('obfuscapk/obfuscators/opcode_injection/opcodes2.txt', 'r') as fp:
            op = fp.read()

        for a in op.split('\n')[:-1]:
            to_return.append(a.split()[0])

        return to_return

    def choose_op_to_insert(self):
        op = self.get_opcode_list()
        idx_random = {random.randint(0, len(op)-1) for _ in range(57)}

        # return [op[i] for i in idx_random]
        # return apis[random.randint(0, len(apis) - 1)]
        opcodes = []
        opc = [op[i] for i in idx_random]
        for _ in range(200):
            el = random.choice(opc)
            opcodes.append(el)
        
        # print("opcodes ", opcodes)
        
        return opcodes
    
    def create_inj(self):
        opcodes = self.choose_op_to_insert()
        injection = ""
        for o in opcodes:
            if '/2addr' in o: 
                # if the opcode takes two addresses
                injection += '\t\t{0} v1, v2\n'.format(o)
            else:
                injection += "\t\t{0} v4, v2, v3\n".format(o)

        return injection[:-1]

    def define_function(self):

        # define the static function that will be randomly called
        function_name = util.generate_random_name()
        injection = self.create_inj()

        function_definition = (
            ".method public static {0}()V\n"
            "\t.registers 5\n"
            "\tconst/4 v0, 0x1\n"
            "\tconst v1, 0x8\n"
            "\tconst v2, 0x10\n"
            "\tconst v3, 0x2A\n"
            "\t.line 1\n"
            "\t.prologue\n"
            "\tif-nez v0, :impossible\n"    # impossible if since v0 = 1 != 0 so the :impossible 
                                            # label will be always reached
            "{1}\n"
            "\t:impossible\n"
            "\treturn-void\n"
            ".end method\n"
        ).format(function_name, injection)

        return function_definition, function_name

    def add_call_to_function(self, smali_file):

        function_definition, function_name = self.define_function()

        with util.inplace_edit_file(smali_file) as (input_file, output_file):
            # inserting the static method inside the smali file after # direct methods comment
            for line in input_file:
                if "# direct methods" in line:
                    output_file.write(line)
                    output_file.write(function_definition)
                else:
                    output_file.write(line)

        return function_name

    def add_call(self, smali_file):
        self.logger.debug(
            'Inserting call to empty function in file "{0}"'.format(smali_file))
        function_name = self.add_call_to_function(smali_file)

        with util.inplace_edit_file(smali_file) as (input_file, output_file):
            for line in input_file:
                # if a function call is found (invoke-* opcode)
                # the call to empty_function() is injected before.smali the real call
                invoke_match = util.invoke_pattern.match(line)
                if invoke_match and "<init>" not in line:
                    # randomizing invocation
                    if random.choice([True, False]) and random.choice([True, False]):
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
                description="Inserting call to function to sensitive call in smali files"):
            if added_methods < max_methods_to_add:
                self.add_call(smali_file)
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