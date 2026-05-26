from tools.database_intelligence_tools import (
    sql_query_analyzer,
    n_plus_one_query_detector,
    eloquent_optimization_advisor,
    database_index_suggestion_engine,
    migration_rollback_simulator,
    seeder_verification_system,
    database_backup_assistant,
    schema_visualization_engine,
    er_diagram_generator,
    api_documentation_generator,
)


def handle_database_intelligence_routes(user_input: str, text: str, clean_text: str):
    routes = {
        "sql query analyzer": sql_query_analyzer,
        "n plus one query detector": n_plus_one_query_detector,
        "n+1 query detector": n_plus_one_query_detector,
        "eloquent optimization advisor": eloquent_optimization_advisor,
        "database index suggestion engine": database_index_suggestion_engine,
        "migration rollback simulator": migration_rollback_simulator,
        "seeder verification system": seeder_verification_system,
        "database backup assistant": database_backup_assistant,
        "schema visualization engine": schema_visualization_engine,
        "er diagram generator": er_diagram_generator,
        "api documentation generator": api_documentation_generator,
    }

    handler = routes.get(text)
    if handler:
        return handler()

    return None
