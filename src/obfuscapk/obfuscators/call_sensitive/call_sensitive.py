import logging
import random
import re
import string
import os

from obfuscapk import obfuscator_category
from obfuscapk import util
from obfuscapk.obfuscation import Obfuscation


class CallSensitive(obfuscator_category.ICodeObfuscator):

    def __init__(self):
        self.logger = logging.getLogger(
            "{0}.{1}".format(__name__, self.__class__.__name__)
        )
        super().__init__()

    @staticmethod
    def get_sensitive_api():
        to_return = list()
        # print(os.listdir(os.getcwd()))
        with open('obfuscapk/obfuscators/call_sensitive/sensitive_apis.txt', 'r') as fp:
            apis = fp.read()

        for a in apis.split('\n')[:-1]:
            if a.endswith('()V') or a.endswith('()Z') or a.endswith('()I'):
                to_return.append(a)

        return to_return

    def chose_apis_to_call(self):
        apis = self.get_sensitive_api()
        idx_random = {random.randint(0, len(apis)-1) for _ in range(8)}

        return [apis[i] for i in idx_random]
        # return apis[random.randint(0, len(apis) - 1)]

    @staticmethod
    def create_invoke(api):

        invoke = ""
        # if the api contains <init> (i.e. it's a contructor the idea is to invoke new-instace on the class and then call
        # <init>
        if '<init>' in api:
            invoke = (
                "\tnew-instance v1, {0};\n"
                "\tinvoke-direct {{v1}}, {1}\n"
            ).format(api.split(';')[0], api)
        else:
            # otherwise we need to invoke new-instance on the class constructor to instance the object and then call the API
            invoke = (
                "\tnew-instance v1, {0};\n"
                "\tinvoke-direct {{v1}}, {1};-><init>()V\n"
                "\tinvoke-virtual {{v1}}, {2}\n"
            ).format(api.split(';')[0], api.split(';')[0], api)

        return invoke

    def define_function(self, api_call):

        # define the static function that will be randomly called
        function_name = util.generate_random_name()
        invoke = self.create_invoke(api_call)
        function_definition = (
            ".method public static {0}()V\n"
            "\t.registers 3\n"
            "\tconst/4 v0, 0x1\n"
            "\t.line 1\n"
            "\t.prologue\n"
            "\tif-nez v0, :impossible\n"    # impossible if since v0 = 1 is always != 0 so the :impossible 
                                            # label will be always reached
            "{1}\n"
            "\t:impossible\n"
            "\treturn-void\n"
            ".end method\n"
        ).format(function_name, invoke)

        return function_definition, function_name

    def add_call_to_sensitive_function(self, smali_file):

        apis_to_call = self.chose_apis_to_call()
        # api1 = "Lcom/android/camera/util/QuickActivity;-><init>()V"
        # api2 = "Lcom/android/deskclock/DeskClock;->onPause()V"
        # api3 = "Landroid/graphics/drawable/ScaleDrawable;->getIntrinsicWidth()I"
        # apis_to_call = [api1, api2, api3]

        function_names = []
        for api in apis_to_call:
            function_definition, function_name = self.define_function(api)
            function_names.append(function_name)

            with util.inplace_edit_file(smali_file) as (input_file, output_file):
                # inserting the static method inside the smali file after # direct methods comment
                for line in input_file:
                    if "# direct methods" in line:
                        output_file.write(line)
                        output_file.write(function_definition)
                    else:
                        output_file.write(line)

        return function_names

    def add_call_to_emtpy(self, smali_file):
        self.logger.debug(
            'Inserting call to empty function in file "{0}"'.format(smali_file))
        function_names = self.add_call_to_sensitive_function(smali_file)

        with util.inplace_edit_file(smali_file) as (input_file, output_file):
            for line in input_file:
                # if a function call is found (invoke-* opcode)
                # the call to empty_function() is injected before.smali the real call
                invoke_match = util.invoke_pattern.match(line)
                if invoke_match:
                    # randomizing invocation
                    if random.choice([True, False]) and random.choice([True, False]):
                        function_name = function_names[random.randint(0, len(function_names))-1]
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
