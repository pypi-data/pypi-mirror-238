from typing import Dict

import prettytable as prettytable

default_title_config = {
    'key': {
        'title': 'Event',
        'max_width': 10,
    },
    'value': {
        'title': 'Details',
        'max_width': 10,
    }
}


def create_key_value_table(data, data_config: Dict, title_config: Dict = None, footer: bool = False):
    if title_config is None:
        title_config = default_title_config

    table = prettytable.PrettyTable([item['title'] for item in title_config.values()])
    table._max_width = {item['title']: item['max_width'] for item in title_config.values()}

    for item in title_config.values():
        table.align[item['title']] = item.get('align', 'c')

    for attr, config in data_config.items():
        key = config['display_name']
        value = config['formatter'](getattr(data, attr))
        table.add_row((key, value))

    table = table.get_string()

    if footer:
        table = with_table_footer(table)

    return table


def create_key_value_table_from_dict(data: Dict, data_config: Dict, title_config: Dict = None, footer: bool = False):
    class dummy:
        def __init__(self):
            super().__init__()
            for k, v in data.items():
                self.__setattr__(k, v)

    return create_key_value_table(dummy(), data_config, title_config, footer)


def create_key_value_tables(data, data_config: Dict, title_config: Dict = None, footer: bool = False):
    tables = []

    for row in data:
        table = create_key_value_table(row, data_config, title_config, footer)
        tables.append(table)

    return '\n\n'.join(tables)


def with_table_footer(table: str):
    list_of_table_lines = table.split('\n')
    horizontal_line = list_of_table_lines[0]
    result_lines = 1
    msg = "\n".join(list_of_table_lines[:-(result_lines + 1)])
    msg += f'\n{horizontal_line}\n'
    msg += "\n".join(list_of_table_lines[-(result_lines + 1):])
    return msg


def default_formatter(x):
    return x


def date_formatter(x):
    try:
        return x.strftime('%d %b')
    except AttributeError:
        return x
