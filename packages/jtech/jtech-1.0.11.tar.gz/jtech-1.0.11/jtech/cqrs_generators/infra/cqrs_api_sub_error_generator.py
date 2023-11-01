import jtech.utils.dir_constants as src
import jtech.utils.tpl_constants as tpl
from jtech.generator.code_generator import CodeGenerator


class CqrsApiSubErrorGenerator(CodeGenerator):
    """
    Generate API Sub Error
    """

    def get_target(self):
        return "ApiSubError.java"

    def get_template(self):
        return tpl.CQRS_API_SUB_ERROR

    def get_source(self):
        return src.CQRS_INFRA_EXCEPTIONS
