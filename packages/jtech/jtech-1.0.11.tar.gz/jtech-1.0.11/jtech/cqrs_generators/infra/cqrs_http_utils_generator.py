import jtech.utils.dir_constants as src
import jtech.utils.tpl_constants as tpl
from jtech.generator.code_generator import CodeGenerator


class CqrsHttpUtilsGenerator(CodeGenerator):
    """
    Generate Http Utils
    """

    def get_target(self):
        return "HttpUtils.java"

    def get_template(self):
        return tpl.CQRS_HTTP_UTILS

    def get_source(self):
        return src.CQRS_UTILS
