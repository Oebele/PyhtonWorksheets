import ast
import base64
import getopt
import io
import signal
import sys

from contextlib import contextmanager


class TimeoutException(Exception):
    pass


@contextmanager
def time_limit(seconds):
    def signal_handler(signum, frame):
        raise TimeoutException('Timed out!')
    signal.signal(signal.SIGALRM, signal_handler)
    signal.alarm(seconds)
    try:
        yield
    finally:
        signal.alarm(0)


class Interpreter(object):

    def __init__(self):
        self.env = {}
        self.out_save = sys.stdout
        self.err_save = sys.stderr

    def redirect_output(self):
        self.out = io.StringIO()
        self.err = io.StringIO()
        sys.stdout = self.out
        sys.stderr = self.err

    def reset_output(self):
        self.out.close()
        self.out.close()
        sys.stdout = self.out_save
        sys.stderr = self.err_save

    def executeString(self, code_string):
        return_values = []
        try:
            tree = ast.parse(code_string)
        except Exception as e:
            return [self.create_response(0, 1, '', '', str(e))]

        lines = code_string.splitlines()

        if hasattr(tree, 'body'):
            for node in tree.body:
                return_value = self.executeNode(node, lines)
                return_values.append(return_value)

        self.env = {}
        return return_values

    def executeNode(self, node, lines):
        self.redirect_output()
        try:
            compile_mode = self.determine_compile_node(node)
            begin, end, code_snippet = self.create_code_snippet(node, lines)
            code_object = compile(code_snippet, '<string>', compile_mode)
            with time_limit(3):
                return_value = eval(code_object, self.env, self.env)
            output_string = self.out.getvalue()
            error_string = self.err.getvalue()
        except Exception as e:
            return_value = ''
            output_string = ''
            error_string = str(e)
        finally:
            self.reset_output()

        return self.create_response(begin, end, return_value,
                                    output_string, error_string)

    def create_response(self, begin, end, return_value,
                        output_string, error_string):

        return_value = self.clean_up(return_value)
        output_string = self.clean_up(output_string)
        error_string = self.clean_up(error_string)

        return {
            'begin': begin,
            'end': end,
            'return_value': return_value,
            'output_string': output_string,
            'error_string': error_string
        }

    def create_code_snippet(self, node, lines):
        start_index, end_index = self.get_end_line(node, lines)
        if isinstance(node, ast.Expr):
            return start_index, end_index, ' '.join(
                lines[start_index: end_index])

        return start_index, end_index, '\n'.join(
            lines[start_index: end_index])

    def get_end_line(self, node, lines):
        if self.statement_is_not_a_expression(node):
            return node.lineno - 1, self.get_end_line(node.body[-1], lines)[1]

        line_index = node.lineno - 1
        if self.statement_is_multiline_string(node, lines, line_index):
            return self.process_multiline_string(lines, line_index, node)

        line_index = self.process_multiline_expressions(lines, line_index)
        return node.lineno - 1, line_index

    def statement_is_not_a_expression(self, node):
        return hasattr(node, 'body')

    def statement_is_multiline_string(self, node, lines, line_index):
        return isinstance(node, ast.Expr) \
            and lines[line_index].count('"""') == 1

    def process_multiline_string(self, lines, line_index, node):
        start = line_index - 1
        for i in range(start, -1, -1):
            if lines[i].count('"""') > 0:
                return i, node.lineno
        return 0, node.lineno

    def process_multiline_expressions(self, lines, line_index):
        open_braces = 0
        open_brackets = 0
        open_curly_braces = 0
        constains_backslash = True
        while self.should_go_on(lines, open_braces,
                                open_brackets, open_curly_braces,
                                constains_backslash, line_index):
            line = lines[line_index]
            open_braces += line.count('(') - line.count(')')
            open_brackets += line.count('[') - line.count(']')
            open_curly_braces += line.count('{') - line.count('}')
            backslashes = line.count('\\')
            constains_backslash = backslashes > 0 and backslashes % 0 == 0
            line_index += 1
        return line_index

    def should_go_on(self, lines, open_braces, open_brackets,
                     open_curly_braces, constains_backslash, line_index):
        return (
                    (
                        constains_backslash or
                        open_curly_braces > 0 or
                        open_brackets > 0 or
                        open_braces > 0
                    ) and
                    line_index < len(lines)
        )

    def clean_up(self, return_value):
        try:
            return '' if return_value is None else \
                str(return_value).replace('\n', ' ').strip()
        except:
            return repr(return_value)

    def determine_compile_node(self, node):
        return 'eval' if isinstance(node, ast.Expr) else 'exec'


def main():
    source_code = parse_arguments()
    if source_code is None:
        print('No source code')
        return
    interpreter = Interpreter()
    result = interpreter.executeString(source_code)
    print(result)


def parse_arguments():
    opts, args = getopt.getopt(sys.argv[1:], 's:b:')

    for opt, arg in opts:
        if opt == '-s':
            return arg
        if opt == '-b':
            return base64.b64decode(arg).decode('utf-8')
    return None


if __name__ == "__main__":
    main()
