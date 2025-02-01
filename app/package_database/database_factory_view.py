

import sqlalchemy as sa
from sqlalchemy.ext.compiler import compiles
from sqlalchemy.schema import DDLElement
from sqlalchemy.sql import table


# Create view class  
class CreateView(DDLElement):
    def __init__(self, name, selectable):
        self.name = name
        self.selectable = selectable

#Drop view class
class DropView(DDLElement):
    def __init__(self, name):
        self.name = name


# Compilation process

@compiles(CreateView)
def _create_view(element, compiler, **kw):
    return f"CREATE VIEW {element.name} AS {compiler.sql_compiler.process(element.selectable, literal_binds=True)}"

@compiles(DropView)
def _drop_view(element, compiler, **kw):
    return f"DROP VIEW {element.name}"



