import psycopg2
import json
import hashlib
from psycopg2 import Error


class Dbversion:
    def __init__(self, host, user, database, schema, password):
  
        self.host = host
        self.user = user
        self.database = database
        self.password = password
        self.schema = schema
    
    
    def get_dbversion_report(self):
        
        report = ""

        connection = None

        try:            
            connection =  psycopg2.connect(
                host=self.host,
                user=self.user,
                database=self.database,
                password=self.password
            )

            if connection.closed == 0:  # 0 means the connection is open                
              
                cursor = connection.cursor()
                cursor.execute("select version(); ")
                record = cursor.fetchone()
                print("You're connected to database: ", record)
                              
                for queryName, queryStatement in self.sqls.items():         

                    queryStatement = queryStatement.replace("%schema_name", "'" + self.schema + "' ")

                    cursor.execute(queryStatement)
                    rows = cursor.fetchall()
                    
                    report = report + "--------------------------------------------" + "\r\n"
                    report = report + queryName + ":" + str(cursor.rowcount) +  "\r\n"
                    report = report + "--------------------------------------------" + "\r\n"
     

                    report = report + self.to_json(cursor, rows) + "\r\n" 
                    report = report + "\r\n\r\n"
                
                report = report.strip()          
        except Error as e:
            print("Error while connecting to Postgresql", e)
            raise
        finally:
            # Closing the connection
            if connection.closed == 0:
                cursor.close()
                connection.close()
                print("Postgresql connection is closed")

        return report

    
    def calculate_hash(self, text):
        # Create a new hash object using the specified algorithm
        algorithm='sha256'
        hash_object = hashlib.new(algorithm)
        
        # Update the hash object with the bytes of the text
        hash_object.update(text.encode())

        # Return the hexadecimal digest of the hash
        return hash_object.hexdigest()
    
    def to_json(self, cursor, rows):
        # Assuming you know the column names
        column_names = [description[0] for description in cursor.description]

        # Convert each row to JSON
        json_data = []
        for row in rows:
            row_dict = dict(zip(column_names, row))
            json_row = json.dumps(row_dict)
            json_data.append(json_row)

        return "\r\n".join(json_data)

# ----------------------------------------------------
# You man need to remove some of the SQL statements that represent something that is not
# related to database versioning.
# ----------------------------------------------------

    sqls = {
"0":
"""
SELECT c.oid, c.fdwowner, c.fdwoptions, c.foreign_data_wrapper_catalog, c.foreign_data_wrapper_name, c.authorization_identifier, c.foreign_data_wrapper_language
FROM information_schema._pg_foreign_data_wrappers c
ORDER BY c.oid, c.fdwowner, c.fdwoptions, c.foreign_data_wrapper_catalog, c.foreign_data_wrapper_name, c.authorization_identifier, c.foreign_data_wrapper_language;
"""
, 

"1":
"""
SELECT c.oid, c.srvoptions, c.foreign_server_catalog, c.foreign_server_name, c.foreign_data_wrapper_catalog, c.foreign_data_wrapper_name, c.foreign_server_type, c.foreign_server_version, c.authorization_identifier
FROM information_schema._pg_foreign_servers c
ORDER BY c.oid, c.srvoptions, c.foreign_server_catalog, c.foreign_server_name, c.foreign_data_wrapper_catalog, c.foreign_data_wrapper_name, c.foreign_server_type, c.foreign_server_version, c.authorization_identifier;
"""
, 

"2":
"""
SELECT c.nspname, c.relname, c.attname, c.attfdwoptions
FROM information_schema._pg_foreign_table_columns c
ORDER BY c.nspname, c.relname, c.attname, c.attfdwoptions;
"""
, 

"3":
"""
SELECT c.foreign_table_catalog, c.foreign_table_schema, c.foreign_table_name, c.ftoptions, c.foreign_server_catalog, c.foreign_server_name, c.authorization_identifier
FROM information_schema._pg_foreign_tables c
ORDER BY c.foreign_table_catalog, c.foreign_table_schema, c.foreign_table_name, c.ftoptions, c.foreign_server_catalog, c.foreign_server_name, c.authorization_identifier;
"""
, 

"4":
"""
SELECT c.oid, c.umoptions, c.umuser, c.authorization_identifier, c.foreign_server_catalog, c.foreign_server_name, c.srvowner
FROM information_schema._pg_user_mappings c
ORDER BY c.oid, c.umoptions, c.umuser, c.authorization_identifier, c.foreign_server_catalog, c.foreign_server_name, c.srvowner;
"""
, 

"5":
"""
SELECT c.grantee, c.role_name, c.is_grantable
FROM information_schema.administrable_role_authorizations c
ORDER BY c.grantee, c.role_name, c.is_grantable;
"""
, 

"6":
"""
SELECT c.grantee, c.role_name, c.is_grantable
FROM information_schema.applicable_roles c
ORDER BY c.grantee, c.role_name, c.is_grantable;
"""
, 

"7":
"""
SELECT c.udt_catalog, c.udt_schema, c.udt_name, c.attribute_name, c.ordinal_position, c.attribute_default, c.is_nullable, c.data_type, c.character_maximum_length, c.character_octet_length, c.character_set_catalog, c.character_set_schema, c.character_set_name, c.collation_catalog, c.collation_schema, c.collation_name, c.numeric_precision, c.numeric_precision_radix, c.numeric_scale, c.datetime_precision, c.interval_type, c.interval_precision, c.attribute_udt_catalog, c.attribute_udt_schema, c.attribute_udt_name, c.scope_catalog, c.scope_schema, c.scope_name, c.maximum_cardinality, c.dtd_identifier, c.is_derived_reference_attribute
FROM information_schema.attributes c
where c.udt_name not like '\_\_%'
ORDER BY c.udt_catalog, c.udt_schema, c.udt_name, c.attribute_name, c.ordinal_position, c.attribute_default, c.is_nullable, c.data_type, c.character_maximum_length, c.character_octet_length, c.character_set_catalog, c.character_set_schema, c.character_set_name, c.collation_catalog, c.collation_schema, c.collation_name, c.numeric_precision, c.numeric_precision_radix, c.numeric_scale, c.datetime_precision, c.interval_type, c.interval_precision, c.attribute_udt_catalog, c.attribute_udt_schema, c.attribute_udt_name, c.scope_catalog, c.scope_schema, c.scope_name, c.maximum_cardinality, c.dtd_identifier, c.is_derived_reference_attribute;
"""
, 

"8":
"""
SELECT c.character_set_catalog, c.character_set_schema, c.character_set_name, c.character_repertoire, c.form_of_use, c.default_collate_catalog, c.default_collate_schema, c.default_collate_name
FROM information_schema.character_sets c
ORDER BY c.character_set_catalog, c.character_set_schema, c.character_set_name, c.character_repertoire, c.form_of_use, c.default_collate_catalog, c.default_collate_schema, c.default_collate_name;
"""
, 

"9":
"""
SELECT c.constraint_catalog, c.constraint_schema, c.constraint_name, c.specific_catalog, c.specific_schema, c.specific_name
FROM information_schema.check_constraint_routine_usage c
ORDER BY c.constraint_catalog, c.constraint_schema, c.constraint_name, c.specific_catalog, c.specific_schema, c.specific_name;
"""
, 

"10":
"""
SELECT c.constraint_catalog, c.constraint_schema, c.constraint_name, c.check_clause
FROM information_schema.check_constraints c
ORDER BY c.constraint_catalog, c.constraint_schema, c.constraint_name, c.check_clause;
"""
, 

"11":
"""
SELECT c.collation_catalog, c.collation_schema, c.collation_name, c.character_set_catalog, c.character_set_schema, c.character_set_name
FROM information_schema.collation_character_set_applicability c
ORDER BY c.collation_catalog, c.collation_schema, c.collation_name, c.character_set_catalog, c.character_set_schema, c.character_set_name;
"""
, 

"12":
"""
SELECT c.collation_catalog, c.collation_schema, c.collation_name, c.pad_attribute
FROM information_schema.collations c
ORDER BY c.collation_catalog, c.collation_schema, c.collation_name, c.pad_attribute;
"""
, 

"13":
"""
SELECT c.table_catalog, c.table_schema, c.table_name, c.column_name, c.dependent_column
FROM information_schema.column_column_usage c
WHERE table_schema =  %schema_name
and c.TABLE_NAME not like '\_\_%'
And c.COLUMN_NAME not like '\_\_%'
ORDER BY c.table_catalog, c.table_schema, c.table_name, c.column_name, c.dependent_column;
"""
, 

"14":
"""
SELECT c.domain_catalog, c.domain_schema, c.domain_name, c.table_catalog, c.table_schema, c.table_name, c.column_name
FROM information_schema.column_domain_usage c
WHERE table_schema =  %schema_name
and c.TABLE_NAME not like '\_\_%'
And c.COLUMN_NAME not like '\_\_%'
ORDER BY c.domain_catalog, c.domain_schema, c.domain_name, c.table_catalog, c.table_schema, c.table_name, c.column_name;
"""
, 

"15":
"""
SELECT c.table_catalog, c.table_schema, c.table_name, c.column_name, c.option_name, c.option_value
FROM information_schema.column_options c
WHERE table_schema =  %schema_name
and c.TABLE_NAME not like '\_\_%'
And c.COLUMN_NAME not like '\_\_%'
ORDER BY c.table_catalog, c.table_schema, c.table_name, c.column_name, c.option_name, c.option_value;
"""
, 

"16":
"""
SELECT c.grantor, c.grantee, c.table_catalog, c.table_schema, c.table_name, c.column_name, c.privilege_type, c.is_grantable
FROM information_schema.column_privileges c
WHERE table_schema =  %schema_name
and c.TABLE_NAME not like '\_\_%'
And c.COLUMN_NAME not like '\_\_%'
ORDER BY c.grantor, c.grantee, c.table_catalog, c.table_schema, c.table_name, c.column_name, c.privilege_type, c.is_grantable;
"""
, 

"17":
"""
SELECT c.udt_catalog, c.udt_schema, c.udt_name, c.table_catalog, c.table_schema, c.table_name, c.column_name
FROM information_schema.column_udt_usage c
WHERE table_schema =  %schema_name
and c.TABLE_NAME not like '\_\_%'
And c.COLUMN_NAME not like '\_\_%'
and c.udt_name not like '\_\_%'
ORDER BY c.udt_catalog, c.udt_schema, c.udt_name, c.table_catalog, c.table_schema, c.table_name, c.column_name;
"""
, 

"18":
"""
SELECT c.table_catalog, c.table_schema, c.table_name, c.column_name, c.ordinal_position, c.column_default, c.is_nullable, c.data_type, c.character_maximum_length, c.character_octet_length, c.numeric_precision, c.numeric_precision_radix, c.numeric_scale, c.datetime_precision, c.interval_type, c.interval_precision, c.character_set_catalog, c.character_set_schema, c.character_set_name, c.collation_catalog, c.collation_schema, c.collation_name, c.domain_catalog, c.domain_schema, c.domain_name, c.udt_catalog, c.udt_schema, c.udt_name, c.scope_catalog, c.scope_schema, c.scope_name, c.maximum_cardinality, c.dtd_identifier, c.is_self_referencing, c.is_identity, c.identity_generation, c.identity_start, c.identity_increment, c.identity_maximum, c.identity_minimum, c.identity_cycle, c.is_generated, c.generation_expression, c.is_updatable
FROM information_schema.columns c
WHERE table_schema =  %schema_name
and c.TABLE_NAME not like '\_\_%'
And c.COLUMN_NAME not like '\_\_%'
and c.udt_name not like '\_\_%'
ORDER BY c.table_catalog, c.table_schema, c.table_name, c.column_name, c.ordinal_position, c.column_default, c.is_nullable, c.data_type, c.character_maximum_length, c.character_octet_length, c.numeric_precision, c.numeric_precision_radix, c.numeric_scale, c.datetime_precision, c.interval_type, c.interval_precision, c.character_set_catalog, c.character_set_schema, c.character_set_name, c.collation_catalog, c.collation_schema, c.collation_name, c.domain_catalog, c.domain_schema, c.domain_name, c.udt_catalog, c.udt_schema, c.udt_name, c.scope_catalog, c.scope_schema, c.scope_name, c.maximum_cardinality, c.dtd_identifier, c.is_self_referencing, c.is_identity, c.identity_generation, c.identity_start, c.identity_increment, c.identity_maximum, c.identity_minimum, c.identity_cycle, c.is_generated, c.generation_expression, c.is_updatable;
"""
, 

"19":
"""
SELECT c.table_catalog, c.table_schema, c.table_name, c.column_name, c.constraint_catalog, c.constraint_schema, c.constraint_name
FROM information_schema.constraint_column_usage c
WHERE table_schema =  %schema_name
and c.TABLE_NAME not like '\_\_%'
And c.COLUMN_NAME not like '\_\_%'
ORDER BY c.table_catalog, c.table_schema, c.table_name, c.column_name, c.constraint_catalog, c.constraint_schema, c.constraint_name;
"""
, 

"20":
"""
SELECT c.table_catalog, c.table_schema, c.table_name, c.constraint_catalog, c.constraint_schema, c.constraint_name
FROM information_schema.constraint_table_usage c
WHERE table_schema =  %schema_name
and c.TABLE_NAME not like '\_\_%'
ORDER BY c.table_catalog, c.table_schema, c.table_name, c.constraint_catalog, c.constraint_schema, c.constraint_name;
"""
, 

"21":
"""
SELECT c.object_catalog, c.object_schema, c.object_name, c.object_type, c.dtd_identifier
FROM information_schema.data_type_privileges c
where c.object_name not like '\_\_%'
ORDER BY c.object_catalog, c.object_schema, c.object_name, c.object_type, c.dtd_identifier;
"""
, 

"22":
"""
SELECT c.constraint_catalog, c.constraint_schema, c.constraint_name, c.domain_catalog, c.domain_schema, c.domain_name, c.is_deferrable, c.initially_deferred
FROM information_schema.domain_constraints c
ORDER BY c.constraint_catalog, c.constraint_schema, c.constraint_name, c.domain_catalog, c.domain_schema, c.domain_name, c.is_deferrable, c.initially_deferred;
"""
, 

"23":
"""
SELECT c.udt_catalog, c.udt_schema, c.udt_name, c.domain_catalog, c.domain_schema, c.domain_name
FROM information_schema.domain_udt_usage c
where c.udt_name not like '\_\_%'
ORDER BY c.udt_catalog, c.udt_schema, c.udt_name, c.domain_catalog, c.domain_schema, c.domain_name;
"""
, 

"24":
"""
SELECT c.domain_catalog, c.domain_schema, c.domain_name, c.data_type, c.character_maximum_length, c.character_octet_length, c.character_set_catalog, c.character_set_schema, c.character_set_name, c.collation_catalog, c.collation_schema, c.collation_name, c.numeric_precision, c.numeric_precision_radix, c.numeric_scale, c.datetime_precision, c.interval_type, c.interval_precision, c.domain_default, c.udt_catalog, c.udt_schema, c.udt_name, c.scope_catalog, c.scope_schema, c.scope_name, c.maximum_cardinality, c.dtd_identifier
FROM information_schema.domains c
where c.udt_name not like '\_\_%'
ORDER BY c.domain_catalog, c.domain_schema, c.domain_name, c.data_type, c.character_maximum_length, c.character_octet_length, c.character_set_catalog, c.character_set_schema, c.character_set_name, c.collation_catalog, c.collation_schema, c.collation_name, c.numeric_precision, c.numeric_precision_radix, c.numeric_scale, c.datetime_precision, c.interval_type, c.interval_precision, c.domain_default, c.udt_catalog, c.udt_schema, c.udt_name, c.scope_catalog, c.scope_schema, c.scope_name, c.maximum_cardinality, c.dtd_identifier;
"""
, 

"25":
"""
SELECT c.object_catalog, c.object_schema, c.object_name, c.object_type, c.collection_type_identifier, c.data_type, c.character_maximum_length, c.character_octet_length, c.character_set_catalog, c.character_set_schema, c.character_set_name, c.collation_catalog, c.collation_schema, c.collation_name, c.numeric_precision, c.numeric_precision_radix, c.numeric_scale, c.datetime_precision, c.interval_type, c.interval_precision, c.domain_default, c.udt_catalog, c.udt_schema, c.udt_name, c.scope_catalog, c.scope_schema, c.scope_name, c.maximum_cardinality, c.dtd_identifier
FROM information_schema.element_types c
where c.object_name not like '\_\_%'
and c.udt_name not like '\_\_%'
ORDER BY c.object_catalog, c.object_schema, c.object_name, c.object_type, c.collection_type_identifier, c.data_type, c.character_maximum_length, c.character_octet_length, c.character_set_catalog, c.character_set_schema, c.character_set_name, c.collation_catalog, c.collation_schema, c.collation_name, c.numeric_precision, c.numeric_precision_radix, c.numeric_scale, c.datetime_precision, c.interval_type, c.interval_precision, c.domain_default, c.udt_catalog, c.udt_schema, c.udt_name, c.scope_catalog, c.scope_schema, c.scope_name, c.maximum_cardinality, c.dtd_identifier;
"""
, 

"26":
"""
SELECT c.role_name
FROM information_schema.enabled_roles c
ORDER BY c.role_name;
"""
, 

"27":
"""
SELECT c.foreign_data_wrapper_catalog, c.foreign_data_wrapper_name, c.option_name, c.option_value
FROM information_schema.foreign_data_wrapper_options c
ORDER BY c.foreign_data_wrapper_catalog, c.foreign_data_wrapper_name, c.option_name, c.option_value;
"""
, 

"28":
"""
SELECT c.foreign_data_wrapper_catalog, c.foreign_data_wrapper_name, c.authorization_identifier, c.library_name, c.foreign_data_wrapper_language
FROM information_schema.foreign_data_wrappers c
ORDER BY c.foreign_data_wrapper_catalog, c.foreign_data_wrapper_name, c.authorization_identifier, c.library_name, c.foreign_data_wrapper_language;
"""
, 

"29":
"""
SELECT c.foreign_server_catalog, c.foreign_server_name, c.option_name, c.option_value
FROM information_schema.foreign_server_options c
ORDER BY c.foreign_server_catalog, c.foreign_server_name, c.option_name, c.option_value;
"""
, 

"30":
"""
SELECT c.foreign_server_catalog, c.foreign_server_name, c.foreign_data_wrapper_catalog, c.foreign_data_wrapper_name, c.foreign_server_type, c.foreign_server_version, c.authorization_identifier
FROM information_schema.foreign_servers c
ORDER BY c.foreign_server_catalog, c.foreign_server_name, c.foreign_data_wrapper_catalog, c.foreign_data_wrapper_name, c.foreign_server_type, c.foreign_server_version, c.authorization_identifier;
"""
, 

"31":
"""
SELECT c.foreign_table_catalog, c.foreign_table_schema, c.foreign_table_name, c.option_name, c.option_value
FROM information_schema.foreign_table_options c
ORDER BY c.foreign_table_catalog, c.foreign_table_schema, c.foreign_table_name, c.option_name, c.option_value;
"""
, 

"32":
"""
SELECT c.foreign_table_catalog, c.foreign_table_schema, c.foreign_table_name, c.foreign_server_catalog, c.foreign_server_name
FROM information_schema.foreign_tables c
ORDER BY c.foreign_table_catalog, c.foreign_table_schema, c.foreign_table_name, c.foreign_server_catalog, c.foreign_server_name;
"""
, 

"33":
"""
SELECT c.catalog_name
FROM information_schema.information_schema_catalog_name c
ORDER BY c.catalog_name;
"""
, 

"34":
"""
SELECT c.constraint_catalog, c.constraint_schema, c.constraint_name, c.table_catalog, c.table_schema, c.table_name, c.column_name, c.ordinal_position, c.position_in_unique_constraint
FROM information_schema.key_column_usage c
WHERE table_schema =  %schema_name
and c.TABLE_NAME not like '\_\_%'
And c.COLUMN_NAME not like '\_\_%'
ORDER BY c.constraint_catalog, c.constraint_schema, c.constraint_name, c.table_catalog, c.table_schema, c.table_name, c.column_name, c.ordinal_position, c.position_in_unique_constraint;
"""
, 

"35":
"""
SELECT c.specific_catalog, c.specific_schema, c.specific_name, c.ordinal_position, c.parameter_mode, c.is_result, c.as_locator, c.parameter_name, c.data_type, c.character_maximum_length, c.character_octet_length, c.character_set_catalog, c.character_set_schema, c.character_set_name, c.collation_catalog, c.collation_schema, c.collation_name, c.numeric_precision, c.numeric_precision_radix, c.numeric_scale, c.datetime_precision, c.interval_type, c.interval_precision, c.udt_catalog, c.udt_schema, c.udt_name, c.scope_catalog, c.scope_schema, c.scope_name, c.maximum_cardinality, c.dtd_identifier, c.parameter_default
FROM information_schema.parameters c
where c.udt_name not like '\_\_%'
ORDER BY c.specific_catalog, c.specific_schema, c.specific_name, c.ordinal_position, c.parameter_mode, c.is_result, c.as_locator, c.parameter_name, c.data_type, c.character_maximum_length, c.character_octet_length, c.character_set_catalog, c.character_set_schema, c.character_set_name, c.collation_catalog, c.collation_schema, c.collation_name, c.numeric_precision, c.numeric_precision_radix, c.numeric_scale, c.datetime_precision, c.interval_type, c.interval_precision, c.udt_catalog, c.udt_schema, c.udt_name, c.scope_catalog, c.scope_schema, c.scope_name, c.maximum_cardinality, c.dtd_identifier, c.parameter_default;
"""
, 

"36":
"""
SELECT c.constraint_catalog, c.constraint_schema, c.constraint_name, c.unique_constraint_catalog, c.unique_constraint_schema, c.unique_constraint_name, c.match_option, c.update_rule, c.delete_rule
FROM information_schema.referential_constraints c
ORDER BY c.constraint_catalog, c.constraint_schema, c.constraint_name, c.unique_constraint_catalog, c.unique_constraint_schema, c.unique_constraint_name, c.match_option, c.update_rule, c.delete_rule;
"""
, 

"37":
"""
SELECT c.grantor, c.grantee, c.table_catalog, c.table_schema, c.table_name, c.column_name, c.privilege_type, c.is_grantable
FROM information_schema.role_column_grants c
WHERE table_schema =  %schema_name
and c.TABLE_NAME not like '\_\_%'
And c.COLUMN_NAME not like '\_\_%'
ORDER BY c.grantor, c.grantee, c.table_catalog, c.table_schema, c.table_name, c.column_name, c.privilege_type, c.is_grantable;
"""
, 

"38":
"""
SELECT c.grantor, c.grantee, c.specific_catalog, c.specific_schema, c.specific_name, c.routine_catalog, c.routine_schema, c.routine_name, c.privilege_type, c.is_grantable
FROM information_schema.role_routine_grants c
ORDER BY c.grantor, c.grantee, c.specific_catalog, c.specific_schema, c.specific_name, c.routine_catalog, c.routine_schema, c.routine_name, c.privilege_type, c.is_grantable;
"""
, 

"39":
"""
SELECT c.grantor, c.grantee, c.table_catalog, c.table_schema, c.table_name, c.privilege_type, c.is_grantable, c.with_hierarchy
FROM information_schema.role_table_grants c
WHERE table_schema =  %schema_name
and c.TABLE_NAME not like '\_\_%'
ORDER BY c.grantor, c.grantee, c.table_catalog, c.table_schema, c.table_name, c.privilege_type, c.is_grantable, c.with_hierarchy;
"""
, 

"40":
"""
SELECT c.grantor, c.grantee, c.udt_catalog, c.udt_schema, c.udt_name, c.privilege_type, c.is_grantable
FROM information_schema.role_udt_grants c
where c.udt_name not like '\_\_%'
ORDER BY c.grantor, c.grantee, c.udt_catalog, c.udt_schema, c.udt_name, c.privilege_type, c.is_grantable;
"""
, 

"41":
"""
SELECT c.grantor, c.grantee, c.object_catalog, c.object_schema, c.object_name, c.object_type, c.privilege_type, c.is_grantable
FROM information_schema.role_usage_grants c
where c.object_name not like '\_\_%'
ORDER BY c.grantor, c.grantee, c.object_catalog, c.object_schema, c.object_name, c.object_type, c.privilege_type, c.is_grantable;
"""
, 

"42":
"""
SELECT c.specific_catalog, c.specific_schema, c.specific_name, c.routine_catalog, c.routine_schema, c.routine_name, c.table_catalog, c.table_schema, c.table_name, c.column_name
FROM information_schema.routine_column_usage c
WHERE table_schema =  %schema_name
and c.TABLE_NAME not like '\_\_%'
And c.COLUMN_NAME not like '\_\_%'
ORDER BY c.specific_catalog, c.specific_schema, c.specific_name, c.routine_catalog, c.routine_schema, c.routine_name, c.table_catalog, c.table_schema, c.table_name, c.column_name;
"""
, 

"43":
"""
SELECT c.grantor, c.grantee, c.specific_catalog, c.specific_schema, c.specific_name, c.routine_catalog, c.routine_schema, c.routine_name, c.privilege_type, c.is_grantable
FROM information_schema.routine_privileges c
ORDER BY c.grantor, c.grantee, c.specific_catalog, c.specific_schema, c.specific_name, c.routine_catalog, c.routine_schema, c.routine_name, c.privilege_type, c.is_grantable;
"""
, 

"44":
"""
SELECT c.specific_catalog, c.specific_schema, c.specific_name, c.routine_catalog, c.routine_schema, c.routine_name
FROM information_schema.routine_routine_usage c
ORDER BY c.specific_catalog, c.specific_schema, c.specific_name, c.routine_catalog, c.routine_schema, c.routine_name;
"""
, 

"45":
"""
SELECT c.specific_catalog, c.specific_schema, c.specific_name, c.routine_catalog, c.routine_schema, c.routine_name, c.sequence_catalog, c.sequence_schema, c.sequence_name
FROM information_schema.routine_sequence_usage c
where c.sequence_name not like '\_\_%'
ORDER BY c.specific_catalog, c.specific_schema, c.specific_name, c.routine_catalog, c.routine_schema, c.routine_name, c.sequence_catalog, c.sequence_schema, c.sequence_name;
"""
, 

"46":
"""
SELECT c.specific_catalog, c.specific_schema, c.specific_name, c.routine_catalog, c.routine_schema, c.routine_name, c.table_catalog, c.table_schema, c.table_name
FROM information_schema.routine_table_usage c
WHERE table_schema =  %schema_name
and c.TABLE_NAME not like '\_\_%'
ORDER BY c.specific_catalog, c.specific_schema, c.specific_name, c.routine_catalog, c.routine_schema, c.routine_name, c.table_catalog, c.table_schema, c.table_name;
"""
, 

"47":
"""
SELECT c.specific_catalog, c.specific_schema, c.specific_name, c.routine_catalog, c.routine_schema, c.routine_name, c.routine_type, c.module_catalog, c.module_schema, c.module_name, c.udt_catalog, c.udt_schema, c.udt_name, c.data_type, c.character_maximum_length, c.character_octet_length, c.character_set_catalog, c.character_set_schema, c.character_set_name, c.collation_catalog, c.collation_schema, c.collation_name, c.numeric_precision, c.numeric_precision_radix, c.numeric_scale, c.datetime_precision, c.interval_type, c.interval_precision, c.type_udt_catalog, c.type_udt_schema, c.type_udt_name, c.scope_catalog, c.scope_schema, c.scope_name, c.maximum_cardinality, c.dtd_identifier, c.routine_body, c.routine_definition, c.external_name, c.external_language, c.parameter_style, c.is_deterministic, c.sql_data_access, c.is_null_call, c.sql_path, c.schema_level_routine, c.max_dynamic_result_sets, c.is_user_defined_cast, c.is_implicitly_invocable, c.security_type, c.to_sql_specific_catalog, c.to_sql_specific_schema, c.to_sql_specific_name, c.as_locator, c.created, c.last_altered, c.new_savepoint_level, c.is_udt_dependent, c.result_cast_from_data_type, c.result_cast_as_locator, c.result_cast_char_max_length, c.result_cast_char_octet_length, c.result_cast_char_set_catalog, c.result_cast_char_set_schema, c.result_cast_char_set_name, c.result_cast_collation_catalog, c.result_cast_collation_schema, c.result_cast_collation_name, c.result_cast_numeric_precision, c.result_cast_numeric_precision_radix, c.result_cast_numeric_scale, c.result_cast_datetime_precision, c.result_cast_interval_type, c.result_cast_interval_precision, c.result_cast_type_udt_catalog, c.result_cast_type_udt_schema, c.result_cast_type_udt_name, c.result_cast_scope_catalog, c.result_cast_scope_schema, c.result_cast_scope_name, c.result_cast_maximum_cardinality, c.result_cast_dtd_identifier
FROM information_schema.routines c
where c.udt_name not like '\_\_%'
ORDER BY c.specific_catalog, c.specific_schema, c.specific_name, c.routine_catalog, c.routine_schema, c.routine_name, c.routine_type, c.module_catalog, c.module_schema, c.module_name, c.udt_catalog, c.udt_schema, c.udt_name, c.data_type, c.character_maximum_length, c.character_octet_length, c.character_set_catalog, c.character_set_schema, c.character_set_name, c.collation_catalog, c.collation_schema, c.collation_name, c.numeric_precision, c.numeric_precision_radix, c.numeric_scale, c.datetime_precision, c.interval_type, c.interval_precision, c.type_udt_catalog, c.type_udt_schema, c.type_udt_name, c.scope_catalog, c.scope_schema, c.scope_name, c.maximum_cardinality, c.dtd_identifier, c.routine_body, c.routine_definition, c.external_name, c.external_language, c.parameter_style, c.is_deterministic, c.sql_data_access, c.is_null_call, c.sql_path, c.schema_level_routine, c.max_dynamic_result_sets, c.is_user_defined_cast, c.is_implicitly_invocable, c.security_type, c.to_sql_specific_catalog, c.to_sql_specific_schema, c.to_sql_specific_name, c.as_locator, c.created, c.last_altered, c.new_savepoint_level, c.is_udt_dependent, c.result_cast_from_data_type, c.result_cast_as_locator, c.result_cast_char_max_length, c.result_cast_char_octet_length, c.result_cast_char_set_catalog, c.result_cast_char_set_schema, c.result_cast_char_set_name, c.result_cast_collation_catalog, c.result_cast_collation_schema, c.result_cast_collation_name, c.result_cast_numeric_precision, c.result_cast_numeric_precision_radix, c.result_cast_numeric_scale, c.result_cast_datetime_precision, c.result_cast_interval_type, c.result_cast_interval_precision, c.result_cast_type_udt_catalog, c.result_cast_type_udt_schema, c.result_cast_type_udt_name, c.result_cast_scope_catalog, c.result_cast_scope_schema, c.result_cast_scope_name, c.result_cast_maximum_cardinality, c.result_cast_dtd_identifier;
"""
, 

"48":
"""
SELECT c.catalog_name, c.schema_name, c.schema_owner, c.default_character_set_catalog, c.default_character_set_schema, c.default_character_set_name, c.sql_path
FROM information_schema.schemata c
ORDER BY c.catalog_name, c.schema_name, c.schema_owner, c.default_character_set_catalog, c.default_character_set_schema, c.default_character_set_name, c.sql_path;
"""
, 

"49":
"""
SELECT c.sequence_catalog, c.sequence_schema, c.sequence_name, c.data_type, c.numeric_precision, c.numeric_precision_radix, c.numeric_scale, c.start_value, c.minimum_value, c.maximum_value, c.increment, c.cycle_option
FROM information_schema.sequences c
where c.sequence_name not like '\_\_%'
ORDER BY c.sequence_catalog, c.sequence_schema, c.sequence_name, c.data_type, c.numeric_precision, c.numeric_precision_radix, c.numeric_scale, c.start_value, c.minimum_value, c.maximum_value, c.increment, c.cycle_option;
"""
, 

"50":
"""
SELECT c.feature_id, c.feature_name, c.sub_feature_id, c.sub_feature_name, c.is_supported, c.is_verified_by, c.comments
FROM information_schema.sql_features c
ORDER BY c.feature_id, c.feature_name, c.sub_feature_id, c.sub_feature_name, c.is_supported, c.is_verified_by, c.comments;
"""
, 

"51":
"""
SELECT c.implementation_info_id, c.implementation_info_name, c.integer_value, c.character_value, c.comments
FROM information_schema.sql_implementation_info c
ORDER BY c.implementation_info_id, c.implementation_info_name, c.integer_value, c.character_value, c.comments;
"""
, 

"52":
"""
SELECT c.feature_id, c.feature_name, c.is_supported, c.is_verified_by, c.comments
FROM information_schema.sql_parts c
ORDER BY c.feature_id, c.feature_name, c.is_supported, c.is_verified_by, c.comments;
"""
, 

"53":
"""
SELECT c.sizing_id, c.sizing_name, c.supported_value, c.comments
FROM information_schema.sql_sizing c
ORDER BY c.sizing_id, c.sizing_name, c.supported_value, c.comments;
"""
, 

"54":
"""
SELECT c.constraint_catalog, c.constraint_schema, c.constraint_name, c.table_catalog, c.table_schema, c.table_name, c.constraint_type, c.is_deferrable, c.initially_deferred, c.enforced, c.nulls_distinct
FROM information_schema.table_constraints c
WHERE table_schema =  %schema_name
and c.TABLE_NAME not like '\_\_%'
ORDER BY c.constraint_catalog, c.constraint_schema, c.constraint_name, c.table_catalog, c.table_schema, c.table_name, c.constraint_type, c.is_deferrable, c.initially_deferred, c.enforced, c.nulls_distinct;
"""
, 

"55":
"""
SELECT c.grantor, c.grantee, c.table_catalog, c.table_schema, c.table_name, c.privilege_type, c.is_grantable, c.with_hierarchy
FROM information_schema.table_privileges c
WHERE table_schema =  %schema_name
and c.TABLE_NAME not like '\_\_%'
ORDER BY c.grantor, c.grantee, c.table_catalog, c.table_schema, c.table_name, c.privilege_type, c.is_grantable, c.with_hierarchy;
"""
, 

"56":
"""
SELECT c.table_catalog, c.table_schema, c.table_name, c.table_type, c.self_referencing_column_name, c.reference_generation, c.user_defined_type_catalog, c.user_defined_type_schema, c.user_defined_type_name, c.is_insertable_into, c.is_typed, c.commit_action
FROM information_schema.tables c
WHERE table_schema =  %schema_name
and c.TABLE_NAME not like '\_\_%'
ORDER BY c.table_catalog, c.table_schema, c.table_name, c.table_type, c.self_referencing_column_name, c.reference_generation, c.user_defined_type_catalog, c.user_defined_type_schema, c.user_defined_type_name, c.is_insertable_into, c.is_typed, c.commit_action;
"""
, 

"57":
"""
SELECT c.udt_catalog, c.udt_schema, c.udt_name, c.specific_catalog, c.specific_schema, c.specific_name, c.group_name, c.transform_type
FROM information_schema.transforms c
where c.udt_name not like '\_\_%'
ORDER BY c.udt_catalog, c.udt_schema, c.udt_name, c.specific_catalog, c.specific_schema, c.specific_name, c.group_name, c.transform_type;
"""
, 

"58":
"""
SELECT c.trigger_catalog, c.trigger_schema, c.trigger_name, c.event_object_catalog, c.event_object_schema, c.event_object_table, c.event_object_column
FROM information_schema.triggered_update_columns c
ORDER BY c.trigger_catalog, c.trigger_schema, c.trigger_name, c.event_object_catalog, c.event_object_schema, c.event_object_table, c.event_object_column;
"""
, 

"59":
"""
SELECT c.trigger_catalog, c.trigger_schema, c.trigger_name, c.event_manipulation, c.event_object_catalog, c.event_object_schema, c.event_object_table, c.action_order, c.action_condition, c.action_statement, c.action_orientation, c.action_timing, c.action_reference_old_table, c.action_reference_new_table, c.action_reference_old_row, c.action_reference_new_row, c.created
FROM information_schema.triggers c
ORDER BY c.trigger_catalog, c.trigger_schema, c.trigger_name, c.event_manipulation, c.event_object_catalog, c.event_object_schema, c.event_object_table, c.action_order, c.action_condition, c.action_statement, c.action_orientation, c.action_timing, c.action_reference_old_table, c.action_reference_new_table, c.action_reference_old_row, c.action_reference_new_row, c.created;
"""
, 

"60":
"""
SELECT c.grantor, c.grantee, c.udt_catalog, c.udt_schema, c.udt_name, c.privilege_type, c.is_grantable
FROM information_schema.udt_privileges c
where c.udt_name not like '\_\_%'
ORDER BY c.grantor, c.grantee, c.udt_catalog, c.udt_schema, c.udt_name, c.privilege_type, c.is_grantable;
"""
, 

"61":
"""
SELECT c.grantor, c.grantee, c.object_catalog, c.object_schema, c.object_name, c.object_type, c.privilege_type, c.is_grantable
FROM information_schema.usage_privileges c
where c.object_name not like '\_\_%'
ORDER BY c.grantor, c.grantee, c.object_catalog, c.object_schema, c.object_name, c.object_type, c.privilege_type, c.is_grantable;
"""
, 

"62":
"""
SELECT c.user_defined_type_catalog, c.user_defined_type_schema, c.user_defined_type_name, c.user_defined_type_category, c.is_instantiable, c.is_final, c.ordering_form, c.ordering_category, c.ordering_routine_catalog, c.ordering_routine_schema, c.ordering_routine_name, c.reference_type, c.data_type, c.character_maximum_length, c.character_octet_length, c.character_set_catalog, c.character_set_schema, c.character_set_name, c.collation_catalog, c.collation_schema, c.collation_name, c.numeric_precision, c.numeric_precision_radix, c.numeric_scale, c.datetime_precision, c.interval_type, c.interval_precision, c.source_dtd_identifier, c.ref_dtd_identifier
FROM information_schema.user_defined_types c
ORDER BY c.user_defined_type_catalog, c.user_defined_type_schema, c.user_defined_type_name, c.user_defined_type_category, c.is_instantiable, c.is_final, c.ordering_form, c.ordering_category, c.ordering_routine_catalog, c.ordering_routine_schema, c.ordering_routine_name, c.reference_type, c.data_type, c.character_maximum_length, c.character_octet_length, c.character_set_catalog, c.character_set_schema, c.character_set_name, c.collation_catalog, c.collation_schema, c.collation_name, c.numeric_precision, c.numeric_precision_radix, c.numeric_scale, c.datetime_precision, c.interval_type, c.interval_precision, c.source_dtd_identifier, c.ref_dtd_identifier;
"""
, 

"63":
"""
SELECT c.authorization_identifier, c.foreign_server_catalog, c.foreign_server_name, c.option_name, c.option_value
FROM information_schema.user_mapping_options c
ORDER BY c.authorization_identifier, c.foreign_server_catalog, c.foreign_server_name, c.option_name, c.option_value;
"""
, 

"64":
"""
SELECT c.authorization_identifier, c.foreign_server_catalog, c.foreign_server_name
FROM information_schema.user_mappings c
ORDER BY c.authorization_identifier, c.foreign_server_catalog, c.foreign_server_name;
"""
, 

"65":
"""
SELECT c.view_catalog, c.view_schema, c.view_name, c.table_catalog, c.table_schema, c.table_name, c.column_name
FROM information_schema.view_column_usage c
WHERE table_schema =  %schema_name
and c.TABLE_NAME not like '\_\_%'
And c.COLUMN_NAME not like '\_\_%'
ORDER BY c.view_catalog, c.view_schema, c.view_name, c.table_catalog, c.table_schema, c.table_name, c.column_name;
"""
, 

"66":
"""
SELECT c.table_catalog, c.table_schema, c.table_name, c.specific_catalog, c.specific_schema, c.specific_name
FROM information_schema.view_routine_usage c
WHERE table_schema =  %schema_name
and c.TABLE_NAME not like '\_\_%'
ORDER BY c.table_catalog, c.table_schema, c.table_name, c.specific_catalog, c.specific_schema, c.specific_name;
"""
, 

"67":
"""
SELECT c.view_catalog, c.view_schema, c.view_name, c.table_catalog, c.table_schema, c.table_name
FROM information_schema.view_table_usage c
WHERE table_schema =  %schema_name
and c.TABLE_NAME not like '\_\_%'
ORDER BY c.view_catalog, c.view_schema, c.view_name, c.table_catalog, c.table_schema, c.table_name;
"""
, 

"68":
"""
SELECT c.table_catalog, c.table_schema, c.table_name, c.view_definition, c.check_option, c.is_updatable, c.is_insertable_into, c.is_trigger_updatable, c.is_trigger_deletable, c.is_trigger_insertable_into
FROM information_schema.views c
WHERE table_schema =  %schema_name
and c.TABLE_NAME not like '\_\_%'
ORDER BY c.table_catalog, c.table_schema, c.table_name, c.view_definition, c.check_option, c.is_updatable, c.is_insertable_into, c.is_trigger_updatable, c.is_trigger_deletable, c.is_trigger_insertable_into;
"""
, 

"69":"""SELECT c.schemaname, c.tablename, c.indexname, c.tablespace, c.indexdef
FROM pg_catalog.pg_indexes c
WHERE c.schemaname =  %schema_name
and c.tablename not like '\_\_%'
ORDER BY c.schemaname, c.tablename, c.indexname, c.tablespace, c.indexdef;""", 


"70": """SELECT 
  n.nspname AS schema,
  p.proname AS name,
  CASE p.prokind
    WHEN 'f' THEN 'FUNCTION'
    WHEN 'p' THEN 'PROCEDURE'
    WHEN 'a' THEN 'AGGREGATE'
    WHEN 'w' THEN 'WINDOW FUNCTION'
    ELSE 'UNKNOWN'
  END AS type,
  pg_get_function_identity_arguments(p.oid) AS arguments,
  pg_get_functiondef(p.oid) AS definition
FROM pg_proc p
JOIN pg_namespace n ON p.pronamespace = n.oid
WHERE n.nspname NOT IN ('pg_catalog', 'information_schema')
and n.nspname  =  %schema_name
ORDER BY  n.nspname, 
p.proname,
p.prokind; """, 


"71":"""SELECT 
    n.nspname AS table_schema,
    c.relname AS table_name,
    t.tgname AS trigger_name,
    pg_get_triggerdef(t.oid, true) AS definition
FROM pg_trigger t
JOIN pg_class c ON t.tgrelid = c.oid
JOIN pg_namespace n ON c.relnamespace = n.oid
WHERE NOT t.tgisinternal
and n.nspname = %schema_name
ORDER BY table_schema, table_name, trigger_name;
""", 


"72":"""SELECT 
    schemaname AS table_schema,
    tablename AS table_name,
    rulename AS rule_name,
    definition
FROM pg_rules
where schemaname = %schema_name
ORDER BY table_schema, table_name, rule_name;  
""", 


"73":"""SELECT 
    n.nspname AS table_schema,
    c.relname AS table_name,
    r.rulename,
    pg_get_ruledef(r.oid, true) AS definition
FROM pg_rewrite r
JOIN pg_class c ON r.ev_class = c.oid
JOIN pg_namespace n ON c.relnamespace = n.oid
WHERE r.rulename <> '_RETURN'
and n.nspname = %schema_name
ORDER BY table_schema, table_name, r.rulename; """

    # --------------------------------
    # master data, which affect the application logic
    # Pls add any master data below, if any. 
    # "69" : "<sql statement to get the master data>"
    # --------------------------------
    
}
    