import ast
import hashlib
import logging
import traceback
from .entities.file_data import FileData
from .visitors import SealightsVisitor
from .packages import astunparse

log = logging.getLogger(__name__)


class FileScanner(object):

    def calculate_file_signature(self, full_path, rel_path):
        file_data = FileData(rel_path)
        try:
            with open(full_path, 'r') as f:
                code = f.read()
            tree = ast.parse(code)
            file_data.hash = self.calculate_file_hash(tree)
            SealightsVisitor(file_data).visit(tree)
        except SyntaxError as e:
            file_data.error = traceback.format_exc()
            log.error("File ignored due to syntax error. %s. problematic code: (%s)" % (full_path, e.text.strip()))
        except Exception as e:
            file_data.error = traceback.format_exc()
            log.error("Failed creating mapping for file. Ignoring... %s" % full_path)
        return file_data

    def calculate_file_hash(self, node):
        # we parse and unparse the file code to eliminate comments
        m = hashlib.md5()
        m.update(astunparse.unparse(node).encode("utf-8"))
        return m.hexdigest()

