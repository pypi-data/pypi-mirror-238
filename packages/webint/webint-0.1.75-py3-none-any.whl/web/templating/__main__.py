import txt
import web.templating

main = txt.application("web-template", web.templating.__doc__)


@main.register()
class Main:
    def setup(self, add_arg):
        add_arg("args", nargs="*", help="argument(s) passed to template")
        add_arg(
            "-w",
            "--wrap",
            nargs="+",
            dest="wrappers",
            type=open,
            help="wrap in given template(s)",
        )

    def run(self, args, stdin):
        document = web.templating.Template(stdin)(*args.args)
        for wrapper in args.wrappers:
            document = web.templating.Template(wrapper)(document)
        print(document)
