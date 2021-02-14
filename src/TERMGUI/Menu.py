from src.Settings import Settings
from src.Dev import Dev
from src.TERMGUI.Term import Term
from src.TERMGUI.Log import Log

class Menu:

    notice = None

    def __init__(self, title, options, back=True):
        self.title   = title
        self.options = options
        self.back    = back
        Log(f'Menu: "{title}"', 'notice', quiet=True)
        self.create_stack().run()

    def create_stack(self):
        self.stack = [
            self.create_banner(),
            self.create_title(self.title),
            f'',
            self.create_options(self.options),
        ]

        if Menu.notice:
            self.stack.insert(1, "")
            self.stack.insert(1, self.create_notice())
            self.stack.insert(1, "")

        return self

    def create_notice(self):
        result      = f' > > {Menu.notice}'
        Menu.notice = None
        return result

    def show(self, stack, clear=True):
        if clear:
            Term.clear()

        for line in stack:
            print(line)

        return self

    def run(self):
        self.show(self.stack)
        return self

    def create_banner(self):
        title = [
            f'##################################################',
            f'LOFSongManager V{Settings.get_version()}'.center(50),
            f'##################################################',
        ]

        if Dev.isDev():
            title.insert(0, self.create_dev_banner())

        return "\n".join(title)

    def create_title(self, title):
        return f':: {title}'

    def create_dev_banner(self):
        dev_banner = f'Development Mode'.center(50)
        dev_banner = f'##{dev_banner[2:-2]}##'
        return dev_banner

    def create_options(self, options):
        stack = []

        for i, option in enumerate(options, start=1):
            if (i < 10):
                stack.append(f'    {i}) {option}')
            elif (i < 100):
                stack.append(f'   {i}) {option}')
            else:
                stack.append(f'  {i}) {option}')

        stack.append(f'')

        if self.back:
            stack.append(f'   b) Back')
            stack.append(f'')

        return "\n".join(stack)

    def get_result(self):
        ans = input(f'   : ').lower()


        if ans == "b" and self.back:
            Log(f'Menu Answer: "back"', 'sub', quiet=True)
            print(f'')
            return "back"
        elif ans.isnumeric() and int(ans) <= len(self.options):
            result = (int(ans) -1)
            Log(f'Menu Answer: "{self.options[result]}"', 'sub', quiet=True)
            print(f'')
            return result

        print(f'')
        print(f'"{ans}" is not a valid option!')
        print(f'')
        Log(f'Menu Answer Not Valid!: "{ans}"', 'sub', quiet=True)
        Log.press_enter()

        return self.create_stack().run().get_result()



