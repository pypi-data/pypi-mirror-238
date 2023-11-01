from jinja2 import Template


class TemplateManager(object):
    def __init__(self, context):
        self.context = context

    def __read_template_file(self, path):
        with open(path, "r") as template_file:
            self.content = template_file.read()

    def __create_template(self):
        self.template = Template(self.content)

    def render_template_from_file(self, path):
        self.__read_template_file(path)
        self.__create_template()
        return self.template.render(self.context)

    def render_template(self, content):
        self.content = content
        self.__create_template()
        return self.template.render(self.context)
