from nomad.config.models.plugins import ParserEntryPoint


class NewParserEntryPoint(ParserEntryPoint):
    def load(self):
        from comsol_parser.parsers.parser import NewParser

        return NewParser(**self.dict())


parser_entry_point = NewParserEntryPoint(
    name='NewParser',
    description='New parser entry point configuration.',
    mainfile_name_re=r'.*\.mph',
)
