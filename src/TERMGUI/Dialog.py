import textwrap
from src.TERMGUI.Log import Log

class Dialog:
    def __init__(self, title, body):
        self.stack = [
            f'',
            f'',
            self.create_title(title),
            f'',
            self.create_body(body),
        ]
        self.run()

    def get_mult_choice(self, options):
        if isinstance(options, list):
            optlist = "/".join(options)

        ans = ""
        while not ans in options:
            ans = input(f'  ({optlist}): ').lower()

            if not ans in options:
                print(f'\n  "{ans}" is not a valid option!\n')

        return ans

    def get_result(self, prompt=None):
        return input(f'  {prompt}: ').lower()

    def show(self, stack, clear=True):
        if clear:
            Log.clear()

        for line in stack:
            print(line)

        return self

    def run(self):
        self.show(self.stack)
        return self

    def create_title(self, title):
        return f'  :: {title}'

    def create_body(self, body):
        result = ""

        if isinstance(body, list):
            body = " ".join(body)

        body = body.split("\n ")

        for paragraph in body:
            lines = textwrap.wrap(paragraph, 50, break_long_words=True)
            lines = [ f'     {x}' for x in lines ]
            result += "\n".join(lines)
            result += "\n"

        return result

    def confirm(self):
        self.show([
            f'',
            f'',
            self.create_title("Are you sure?"),
            f'',
            f'',
        ], clear=False)

        ans = self.get_mult_choice(['y','n'])

        if ans == 'y':
            return True
        else:
            return False
