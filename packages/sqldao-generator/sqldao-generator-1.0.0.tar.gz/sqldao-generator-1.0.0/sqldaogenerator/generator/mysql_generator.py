import importlib.resources as pkg_resources
import os
import re
from pathlib import Path
from types import ModuleType

import pandas as pd
from sqlalchemy import create_engine, text

from sqldaogenerator import resources
from sqldaogenerator.generator.enums.MySqlTypeEnum import MySqlTypeEnum
from sqldaogenerator.generator.model.ColumnTemplate import ColumnTemplate
from sqldaogenerator.generator.model.EntityCreateReq import EntityCreateReq


def generate(username: str, password: str, host: str, port: int, database: str,
             datasource_package: ModuleType | str, datasource_name: str,
             base_dao_package: ModuleType | str, base_dao_name: str,
             entities: list[EntityCreateReq], *, override_datasource=False, transaction_name: str = None,
             source_root: str = None):
    datasource_file = get_file_path(datasource_package, datasource_name, source_root=source_root)
    base_dao_file = get_file_path(base_dao_package, base_dao_name, source_root=source_root)
    datasource_package = get_package(datasource_package)
    base_dao_package = get_package(base_dao_package)

    # create a Datasource
    if override_datasource or not datasource_file.is_file():
        template = pkg_resources.files(resources).joinpath('DatasourceTemplate.py').read_text().split('\n')
        scripts = []
        for line in template:
            if line == 'import os':
                continue
            line = (line.replace('Datasource', datasource_name)
                    .replace("os.getenv('username')", f"'{username}'")
                    .replace("os.getenv('password')", f"'{password}'")
                    .replace("os.getenv('host')", f"'{host}'")
                    .replace("os.getenv('port')", f"{port}")
                    .replace("os.getenv('dbname')", f"'{database}'")
                    .replace("os.getenv('echo') == 'True'", 'False')
                    .replace("os.getenv('transaction_name')", f"'{transaction_name}'" if transaction_name else ''))
            scripts.append(line)
        with datasource_file.open('w', encoding='utf-8') as file:
            file.write('\n'.join(scripts))

    # create a BaseDao
    template = pkg_resources.files(resources).joinpath('BaseDaoTemplate.py').read_text().split('\n')
    scripts = []
    for line in template:
        if line == 'from sqldaogenerator.resources.DatasourceTemplate import datasource, Datasource':
            line = f"from {datasource_package}.{datasource_name} import datasource, {datasource_name}"
        else:
            line = (line.replace('BaseDao', base_dao_name)
                    .replace('Datasource', datasource_name))
        scripts.append(line)
    with base_dao_file.open('w', encoding='utf-8') as file:
        file.write('\n'.join(scripts))

    connection_string = f"mysql+mysqlconnector://{username}:{password}@{host}:{port}/{database}"
    engine = create_engine(connection_string, echo=True, pool_recycle=270)
    with engine.connect() as connection:
        results = connection.execute(text(f"""
            select TABLE_NAME, COLUMN_NAME, DATA_TYPE, COLUMN_KEY, COLUMN_COMMENT
            from information_schema.columns 
            where table_name in ('{"','".join(x.table for x in entities)}')
            order by TABLE_NAME, ORDINAL_POSITION
            """)).all()

    for req in entities:
        entity_name = req.entity_name
        entity_file = get_file_path(req.entity_package, entity_name, source_root=source_root)
        criterion_file = get_file_path(req.entity_package, f"{entity_name}Criterion", source_root=source_root)
        dao_file = get_file_path(req.dao_package, f"{entity_name}Dao", source_root=source_root)
        entity_package = get_package(req.entity_package)
        dao_package = get_package(req.dao_package)
        table = req.table

        # create entity, criterion, dao
        camelcased_words = re.findall('[A-Z][a-z0-9]*', entity_name)
        entity_name_underscore = '_'.join(camelcased_words).lower()
        alchemy_columns = []
        columns = []
        modifies = []
        filters = []
        alchemy_types = []
        df = pd.DataFrame(results)
        df = df[df['TABLE_NAME'] == table]
        for i in range(df.shape[0]):
            row = df.iloc[i]
            column_name = row['COLUMN_NAME'].lower()
            data_type = row['DATA_TYPE'].decode() if isinstance(row['DATA_TYPE'], bytes) else row['DATA_TYPE']
            comment = row['COLUMN_COMMENT'].decode() \
                if isinstance(row['COLUMN_COMMENT'], bytes) else row['COLUMN_COMMENT']

            # column
            template = ColumnTemplate.builder(entity_name).column(column_name, data_type).comment(comment)
            if row['COLUMN_KEY'] == 'PRI':
                template.autoincrement().primary_key()
            if template.alchemy_type not in alchemy_types:
                alchemy_types.append(template.alchemy_type)
            alchemy_columns.append(template.build_alchemy_column())

            # fields, filters
            columns.append(template.build_column())
            modifies.append(template.build_modify())
            filters.append(template.build_equal())
            filters.append(template.build_null())
            filters.append(template.build_in())
            if MySqlTypeEnum.is_string(data_type):
                filters.append(template.build_like())
            elif MySqlTypeEnum.is_number(data_type):
                filters.append(template.build_num_compare())
            elif MySqlTypeEnum.is_date(data_type):
                filters.append(template.build_datetime_compare())

        # entity
        tab = '    '
        break_intent = f"\n\n{tab}"
        template = pkg_resources.files(resources).joinpath('EntityTemplate.py').read_text().split('\n')
        scripts = []
        for line in template:
            if line.startswith('from sqlalchemy import Column, '):
                line = f"from sqlalchemy import Column, {', '.join(alchemy_types)}"
            elif line.startswith('    id = Column'):
                scripts.append(tab + f"\n{tab}".join(alchemy_columns) + '\n')
                break
            else:
                line = line.replace('Sample', entity_name).replace('t_sample', table)
            scripts.append(line)
        with entity_file.open('w', encoding='utf-8') as file:
            file.write('\n'.join(scripts))

        # criterion
        template = pkg_resources.files(resources).joinpath('CriterionTemplate.py').read_text().split('\n')
        scripts = []
        go_to = None
        for line in template:
            if go_to:
                if line == go_to:
                    go_to = None
                    line = '\n\n' + line
                else:
                    continue
            if line == 'from sqldaogenerator.resources.DaoTemplate import sample_dao':
                line = f"from {dao_package}.{entity_name}Dao import {entity_name_underscore}_dao"
            elif line == 'from sqldaogenerator.resources.EntityTemplate import Sample':
                line = f"from {entity_package}.{entity_name} import {entity_name}"
            elif line == '    def id(self, group=False, count=False, max=False, min=False, sum=False):':
                line = tab + break_intent.join(columns)
                go_to = '@dataclass'
            elif line == '    def id(self, value: int = None, reverse=False):':
                line = tab + break_intent.join(filters)
                go_to = '@dataclass'
            elif line == '    def id(self, value: int):':
                scripts.append(tab + break_intent.join(modifies) + '\n')
                break
            else:
                line = (line.replace('Sample', entity_name)
                        .replace('sample', entity_name_underscore))
            scripts.append(line)
        with criterion_file.open('w', encoding='utf-8') as file:
            file.write('\n'.join(scripts))

        # dao
        template = pkg_resources.files(resources).joinpath('DaoTemplate.py').read_text().split('\n')
        scripts = []
        query_transactions = ['auto_commit=False', f"name='{transaction_name}'"]
        alter_transactions = [f"name='{transaction_name}'"]
        for line in template:
            if transaction_name:
                if line == '    @transactional(auto_commit=False)':
                    line = f"{tab}@transactional({', '.join(query_transactions)})"
                elif line == '    @transactional()':
                    line = f"{tab}@transactional({', '.join(alter_transactions)})"
            if line == 'from sqldaogenerator.resources.BaseDaoTemplate import BaseDao':
                line = f"from {base_dao_package}.{base_dao_name} import {base_dao_name}"
            elif line == 'from sqldaogenerator.resources.EntityTemplate import Sample':
                line = f"from {entity_package}.{entity_name} import {entity_name}"
            else:
                line = (line.replace('Sample', entity_name)
                        .replace('sample', entity_name_underscore)
                        .replace('BaseDao', base_dao_name))
            scripts.append(line)
        with dao_file.open('w', encoding='utf-8') as file:
            file.write('\n'.join(scripts))


def get_file_path(package: ModuleType | str, name: str, *, source_root: str = None):
    if isinstance(package, str):
        assert source_root, 'The source_root cannot be empty if the package is a string.'
        path = Path(f"{source_root}/{package.replace('.', '/')}")
        if not path.exists():
            os.makedirs(path)
        return path.joinpath(f"{name}.py")
    else:
        return pkg_resources.files(package).joinpath(f"{name}.py")


def get_package(package: ModuleType | str):
    return package if isinstance(package, str) else package.__package__
