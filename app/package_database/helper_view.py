
import sqlalchemy as sa
from sqlalchemy.ext.compiler import compiles
from sqlalchemy.schema import DDLElement
from sqlalchemy.sql import table

from .database_factory_view import CreateView, DropView

# Create the helper to check if the view exists 
def view_exists(ddl, target, connection, **kw):
    return ddl.name in sa.inspect(connection).get_view_names()

def view_doesnt_exist(ddl, target, connection, **kw):
    return not view_exists(ddl, target, connection, **kw)


# Function to create the view
def view(name, metadata, selectable):
    t = table(name)
    t._columns._populate_separate_keys(
        col._make_proxy(t) for col in selectable.selected_columns
    )
    sa.event.listen(
        metadata, "after_create", CreateView(name, selectable).execute_if(callable_=view_doesnt_exist)
    )
    sa.event.listen(
        metadata, "before_drop", DropView(name).execute_if(callable_=view_exists)
    )
    return t
