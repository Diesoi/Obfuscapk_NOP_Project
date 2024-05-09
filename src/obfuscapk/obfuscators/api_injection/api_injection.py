import logging
import random
import string

from obfuscapk import obfuscator_category
from obfuscapk import util
from obfuscapk.obfuscation import Obfuscation

class ApiInjection(obfuscator_category.ICodeObfuscator):
    
    def __init__(self):
        self.logger = logging.getLogger(
            "{0}.{1}".format(__name__, self.__class__.__name__)
        )
        super().__init__()
    
    @staticmethod
    def get_apis():
        to_return = list()
        # print(os.listdir(os.getcwd()))
        with open('obfuscapk/obfuscators/call_sensitive/sensitive_apis.txt', 'r') as fp:
            apis = fp.read()

        for a in apis.split('\n')[:-1]:
            if a.endswith('()V') or a.endswith('()Z') or a.endswith('()I'):
                to_return.append(a)

        return to_return

    def chose_apis_to_call(self):
        apis = self.get_apis()
        idx_random = {random.randint(0, len(apis)-1) for _ in range(8)}

        return [apis[i] for i in idx_random]
    
    @staticmethod
    def api_injection(apis):
        
        injection = ""
        for api in apis:
            if '<init>' in api:
                injection += (
                "\tnew-instance v1, {0};\n"
                "\tinvoke-direct {{v1}}, {1}\n"
            ).format(api.split(';')[0], api)
            else:
                injection += (
                "\tnew-instance v1, {0};\n"
                "\tinvoke-direct {{v1}}, {1};-><init>()V\n"
                "\tinvoke-virtual {{v1}}, {2}\n"
            ).format(api.split(';')[0], api.split(';')[0], api)
        
        return injection

    def add_function(self, smali_file):
        
        # apis = list(self.obfuscation_status.apis_to_inject)
        apis = self.chose_apis_to_call()
        # random name generation for the function
        function_name = util.generate_random_name()
        # string injection definition
        api_inj = self.api_injection(apis)
        # method definition
        function_definition = (
            ".method public static {0}()V\n"
            "\t.registers 3\n"
            "\tconst/4 v0, 0x1\n"
            "\t.line 1\n"
            "\t.prologue\n"
            "\tif-nez v0, :impossible\n"    # impossible if since v0 = 1 is always != 0 so the :impossible label will be always reached
            "{1}\n"
            "\t:impossible\n"
            "\treturn-void\n"
            ".end method\n"
        ).format(function_name, api_inj)

        flag = False
        with util.inplace_edit_file(smali_file) as (input_file, output_file):
            # inserting the static method inside the smali file after # direct methods comment
            for line in input_file:
                if "# direct methods" in line:
                    output_file.write(line)
                    output_file.write(function_definition)
                    flag = True
                else:
                    output_file.write(line)
        return flag
    
    def treat_dex(self, smali_files, max_methods_to_add, interactive):
        added_methods = 0

        for smali_file in util.show_list_progress(
                smali_files,
                interactive=interactive,
                description="Inserting string injection function in smali files"):
            if added_methods < max_methods_to_add:
                if(self.add_function(smali_file)):
                    added_methods += 1
                    return True
                else:
                    continue
            else:
                return False
    
    def obfuscate(self, obfuscation_info: Obfuscation):
        self.logger.info('Running "{0}" obfuscator'.format(self.__class__.__name__))
        self.obfuscation_status = obfuscation_info
        
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
                    if(self.treat_dex(dex_smali_files, max_methods_to_add, obfuscation_info.interactive)):
                        break
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