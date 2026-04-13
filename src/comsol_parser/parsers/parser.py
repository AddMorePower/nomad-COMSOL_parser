import json
import zipfile
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from nomad.datamodel.datamodel import (
        EntryArchive,
    )
    from structlog.stdlib import (
        BoundLogger,
    )

from nomad.config import config
from nomad.parsing.parser import MatchingParser

import comsol_parser.schema_packages.schema_package as comsol

configuration = config.get_plugin_entry_point(
    'comsol_parser.parsers:parser_entry_point'
)


class NewParser(MatchingParser):
    def parse_json(self, data: dict[str, any], previous_node: comsol.Node) -> None:
        if previous_node:
            node = previous_node.m_create(comsol.Node)
        else:
            node = self.sec_data
        node.label = data.get('label', None)
        node.api_class = data.get('apiClass', None)
        node.api_type = data.get('apiType', None)
        node.name = data.get('name', None)
        node.display_label = data.get('displayLabel', None)
        if 'nodes' in data:
            for node_data in data['nodes']:
                self.parse_json(node_data, node)
        if 'settings' in data:
            for setting_info in data['settings']:
                setting = node.m_create(comsol.Setting)
                description = setting_info.get('description', None)
                if isinstance(description, list):
                    setting.description = ','.join(description)
                else:
                    setting.description = description
                setting.name = setting_info.get('name', None)
                setting.value = setting_info.get('value', None)

    def parse(
        self,
        mainfile: str,
        archive: 'EntryArchive',
        logger: 'BoundLogger',
        child_archives: dict[str, 'EntryArchive'] = None,
    ) -> None:
        self.mainfile = mainfile
        self.archive = archive
        with zipfile.ZipFile(self.mainfile, mode='r') as mph:
            data = json.loads(mph.read('smodel.json'))

        self.sec_data = comsol.COMSOLOutput()

        archive.data = self.sec_data

        self.parse_json(data, None)
