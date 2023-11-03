# sqldao-generator

## Easily generate DAOs and Entities from tables

## Notice

- Currently, only MySQL is supported.

## Usage

- For more example, See example/test/generator.py, SampleTest.py

- Create a table first
```sql
create table t_sample
(
    id               bigint unsigned auto_increment comment 'ID'
        primary key,
    column_char      char(32)      null comment 'CHAR',
    column_varchar   varchar(32)   null comment 'VARCHAR',
    column_text      text          null comment 'TEXT',
    column_json      json          null comment 'JSON',
    column_tinyint   tinyint       null comment 'TINYINT',
    column_int       int           null comment 'INT',
    column_double    double(20, 8) null comment 'DOUBLE',
    column_datetime  datetime      null comment 'DATETIME',
    column_timestamp timestamp     null comment 'TIMESTAMP'
)
    comment 'TEST';
```

- Generate a dao and entity from a table

```python
from example import dao, entity
from sqldaogenerator.generator.model.EntityCreateReq import EntityCreateReq
from sqldaogenerator.generator.mysql_generator import generate

entity_tables = [
    ('Sample', 't_sample'),
]

entities = []
for entity_name, table in entity_tables:
    entities.append(EntityCreateReq(entity, entity_name, table, dao))
    or
    entities.append(EntityCreateReq('my.package.entity', entity_name, table, 'my.package.dao'))

generate('username', 'password', 'host', port, 'database',
         datasource_package=dao, datasource_name='Datasource', 
         base_dao_package=dao, base_dao_name='BaseDao', entities=entities,
         override_datasource=True)
or
generate('username', 'password', 'host', port, 'database',
         datasource_package='my.package.dao', datasource_name='Datasource',
         base_dao_package='my.package.dao', base_dao_name='BaseDao', entities=entities,
         override_datasource=True, source_root=r'D:\my\project')
```

- Select

```python
samples, total = (SampleCriterion.builder()
                  .where()
                  .column_char('char2')
                  .column_varchar('varchar')
                  .column_text('text')
                  .column_tinyint(1)
                  .column_int(9)
                  .column_double(123.456)
                  .column_datetime('2023-11-02 09:00:00')
                  .column_timestamp('2023-11-02 09:16:27')
                  .page_no(1)
                  .page_size(10)
                  .order_by('column_datetime desc')
                  .select())
```

- Insert

```python
sample = (SampleCriterion.builder()
          .modify()
          .column_char('char3')
          .column_varchar('varchar')
          .column_text('text')
          .column_json({'abc': 'json'})
          .column_tinyint(1)
          .column_int(10)
          .column_double(123.456)
          .column_datetime('2023-11-02 09:00:00')
          .column_timestamp(datetime.now())
          .insert())
print(sample.id)
```

- Update

```python
updated_count = (SampleCriterion.builder()
                 .modify()
                 .column_char('char0')
                 .column_varchar('varchar0')
                 .column_text('text0')
                 .column_json({'abc': 'json0'})
                 .column_tinyint(10)
                 .column_int(100)
                 .column_double(1230.456)
                 .column_datetime('2023-12-02 09:00:00')
                 .column_timestamp(datetime.now())
                 .where()
                 .id(4)
                 .update())
```

- Delete

```python
deleted_count = (SampleCriterion.builder()
                 .where()
                 .id(4)
                 .delete())
```

- Execute in the same transaction

```python
from sqldaogenerator.common.TransactionManager import transactional


@transactional()
def test_transactional(self):
    insert...
    update...
    delete...
```