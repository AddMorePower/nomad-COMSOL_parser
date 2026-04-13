from typing import (
    TYPE_CHECKING,
)

if TYPE_CHECKING:
    pass

from nomad.config import config
from nomad.datamodel.data import Schema
from nomad.metainfo import MSection, Quantity, SchemaPackage, SectionProxy, SubSection

configuration = config.get_plugin_entry_point(
    'comsol_parser.schema_packages:schema_package_entry_point'
)

m_package = SchemaPackage()


class Setting(MSection):
    description = Quantity(type=str, description='Description of the setting.')
    name = Quantity(type=str, description='Name of the setting.')
    value = Quantity(type=str, description='Value of the setting.')


class Node(MSection):
    label = Quantity(type=str, description='Label of the node.')
    api_class = Quantity(type=str, description='Class of the node.')
    api_type = Quantity(type=str, description='Type of the node.')
    name = Quantity(type=str, description='Name of the node.')
    display_label = Quantity(type=str, description='Display label of the node.')
    nodes = SubSection(
        sub_section=SectionProxy('Node'),
        repeats=True,
        description='Child nodes of the node.',
    )
    settings = SubSection(
        sub_section=Setting.m_def, repeats=True, description='Settings of the node.'
    )


class COMSOLOutput(Schema):
    label = Quantity(type=str, description='Label of the node.')
    api_class = Quantity(type=str, description='Class of the node.')
    api_type = Quantity(type=str, description='Type of the node.')
    name = Quantity(type=str, description='Name of the node.')
    display_label = Quantity(type=str, description='Display label of the node.')
    nodes = SubSection(
        sub_section=Node.m_def, repeats=True, description='Child nodes of the node.'
    )
    settings = SubSection(
        sub_section=Setting.m_def, repeats=True, description='Settings of the node.'
    )


m_package.__init_metainfo__()
