from django.db.backends.ddl_references import Statement, Table

from django_pgrls.state import TenantConstraint

from .settings import original_backend

SQL_ACTIVATE_RLS = """
CREATE POLICY %(policy_name)s ON %(table)s USING (
    CASE
        WHEN current_setting('app.tenant_id', True) is null
        OR current_setting('app.tenant_id') = '%(ALL)s' THEN True
        WHEN current_setting('app.tenant_id') = '%(NONE)s' THEN False
        ELSE %(field_column)s = current_setting('app.tenant_id')::%(column_type)s
    END
);
ALTER TABLE %(table)s ENABLE ROW LEVEL SECURITY;
ALTER TABLE %(table)s FORCE ROW LEVEL SECURITY
"""

SQL_DEACTIVATE_RLS = """
ALTER TABLE %(table)s NO FORCE ROW LEVEL SECURITY;
ALTER TABLE %(table)s DISABLE ROW LEVEL SECURITY;
DROP POLICY IF EXISTS %(policy_name)s on %(table)s
"""


class DatabaseSchemaEditor(original_backend.DatabaseSchemaEditor):
    def _activate_rls(self, model, field_name, policy_name):
        field = model._meta.get_field(field_name)
        field_column = field.get_attname_column()[1]
        column_type = field.cast_db_type(self.connection)

        return Statement(
            SQL_ACTIVATE_RLS,
            table=Table(model._meta.db_table, self.quote_name),
            ALL=TenantConstraint.ALL.value,
            NONE=TenantConstraint.NONE.value,
            field_column=field_column,
            column_type=column_type,
            policy_name=policy_name,
        )

    def _deactivate_rls(self, model, field_name, policy_name):
        return Statement(
            SQL_DEACTIVATE_RLS,
            table=Table(model._meta.db_table, self.quote_name),
            field_name=field_name,
            policy_name=policy_name,
        )
