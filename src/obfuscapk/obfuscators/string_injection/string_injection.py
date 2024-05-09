import logging
import random
import string

from obfuscapk import obfuscator_category
from obfuscapk import util
from obfuscapk.obfuscation import Obfuscation

class StringInjection(obfuscator_category.ICodeObfuscator):
    
    def __init__(self):
        self.logger = logging.getLogger(
            "{0}.{1}".format(__name__, self.__class__.__name__)
        )
        super().__init__()
        
    def string_injection(self, urls):
        string_inj = ""
        
        for i, s in enumerate(urls):
            string_inj += "\tconst-string v{0}, \"{1}\"\n".format(i, s)
        return string_inj
    
    def add_function(self, smali_file, url_to_inject):
    
        # random name generation for the function
        function_name = util.generate_random_name()
        # string injection definition
        string_inj = self.string_injection(url_to_inject)
        # method definition
        function_definition = (
            ".method public static {0}()V\n"
            "\t.registers {1}\n"
            "\t.line 1\n"
            "\t.prologue\n"
            "{2}\n"
            "\treturn-void\n"
            ".end method\n"
        ).format(function_name, len(url_to_inject), string_inj)
        
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
        urls = ['https://www.example.com/6H6D02',
                'https://www.example.com/-07prb4Jy2hg8m3',
                'https://www.example.com/cwnl04rAblC6F',
                'https://www.example.com/cC4DGszTYkF1u',
                'https://www.example.com/4bIDl1rPU4QiC-W',
                'https://www.example.com/3Zz2W6.cefAo',
                'https://www.example.com/3xm5jleCkyzybU-',
                'https://www.example.com/V.Cwb',
                'https://www.example.com/rRywfLivohPxVz2',
                'https://www.example.com/_tr_qYtdatD',
                'https://www.example.com/n46sn5O-3',
                'https://www.example.com/_Gp8fhlmw',
                'https://www.example.com/ZoZWFf2',
                'https://www.example.com/FB6j7BM0',
                'https://www.example.com/hMuzch3suH5T70B',
                'https://www.example.com/ZC8K8a',
                'https://www.example.com/ft-FYdHYTv3og',
                'https://www.example.com/cWwUamj9QvUUX',
                'https://www.example.com/n4skaVeF7Qy-',
                'https://www.example.com/3inK6I',
                'https://www.example.com/D8vG8',
                'https://www.example.com/0ai79VW4N',
                'https://www.example.com/ankYR2.N',
                'https://www.example.com/7mc1t1z',
                'https://www.example.com/-c5nuybvsI.n',
                'https://www.example.com/ISJuB8lOgYArpf',
                'https://www.example.com/6WUdA',
                'https://www.example.com/lofJxmLe-.',
                'https://www.example.com/x4H4KTr',
                'https://www.example.com/zvnwa',
                'https://www.example.com/HNbfaKYU_5gc',
                'https://www.example.com/MQgO503TCRn_jJ2',
                'https://www.example.com/SQg1wwnrjM0In',
                'https://www.example.com/34woabAhR9Nvte',
                'https://www.example.com/8rhoWNe683']
        
        added_methods = 0
        urls_to_inject = [urls[i:i+15] for i in range(0, len(urls), 15)]
        # print(len(urls_to_inject))
        for smali_file in util.show_list_progress(
                smali_files,
                interactive=interactive,
                description="Inserting string injection function in smali files"):
            if added_methods >= len(urls_to_inject):
                break
            if added_methods < max_methods_to_add:
                if(self.add_function(smali_file, urls_to_inject[added_methods])):
                    added_methods += 1
                    # print(smali_file)
                    self.obfuscation_status.ma
                else:
                    continue
            else:
                return False
        return True
    

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