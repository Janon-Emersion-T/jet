from pathlib import Path
import re
import json
import subprocess
from collections import defaultdict

from tools.project_context_tools import get_current_project_path

MAX_OUTPUT = 12000

SKIP_DIRS = {
    ".git", "node_modules", "vendor", "venv", "__pycache__",
    "storage", "bootstrap/cache", "dist", "build", ".next"
}


def _project():
    project = get_current_project_path()
    if not project:
        return None, 'No current project selected.\nUse: use project <path-or-shortcut>'
    return Path(project), None


def _skip(path: Path):
    return any(part in SKIP_DIRS for part in path.parts)


def _read(path: Path):
    return path.read_text(errors="replace")


def _run(cmd, cwd, timeout=60):
    try:
        result = subprocess.run(
            cmd,
            cwd=str(cwd),
            capture_output=True,
            text=True,
            timeout=timeout
        )
        output = result.stdout.strip() or result.stderr.strip() or "No output."
        return output[:MAX_OUTPUT]
    except FileNotFoundError:
        return f"Command not found: {cmd[0]}"
    except Exception as e:
        return f"Command failed: {e}"


def _php_files(project):
    for file in project.rglob("*.php"):
        if not _skip(file):
            yield file


def sql_query_analyzer():
    project, error = _project()
    if error:
        return error

    findings = []

    patterns = [
        r"DB::select\((.*?)\)",
        r"DB::statement\((.*?)\)",
        r"DB::raw\((.*?)\)",
        r"->whereRaw\((.*?)\)",
        r"->orderByRaw\((.*?)\)",
        r"->havingRaw\((.*?)\)",
    ]

    for file in _php_files(project):
        text = _read(file)

        for pattern in patterns:
            matches = re.findall(pattern, text, flags=re.DOTALL)
            for match in matches:
                snippet = " ".join(match.split())[:180]
                risk = "Review manually"

                if "$" in snippet or "request(" in snippet or "input(" in snippet:
                    risk = "Possible dynamic SQL / injection risk"

                findings.append(
                    f"- {file.relative_to(project)}\n"
                    f"  Query: {snippet}\n"
                    f"  Risk: {risk}"
                )

    if not findings:
        return "SQL QUERY ANALYZER — PHASE 241\nNo raw SQL/query risks found."

    return "SQL QUERY ANALYZER — PHASE 241\n\n" + "\n\n".join(findings[:80])


def n_plus_one_query_detector():
    project, error = _project()
    if error:
        return error

    findings = []

    loop_patterns = [
        r"@foreach\s*\((.*?)\)",
        r"foreach\s*\((.*?)\)",
    ]

    relation_access_pattern = r"\$\w+->\w+"

    for file in _php_files(project):
        text = _read(file)
        lines = text.splitlines()

        for i, line in enumerate(lines, start=1):
            if any(re.search(pattern, line) for pattern in loop_patterns):
                window = "\n".join(lines[i:i + 12])

                if re.search(relation_access_pattern, window):
                    findings.append(
                        f"- Possible N+1 risk in {file.relative_to(project)} around line {i}\n"
                        f"  Advice: Check if relationships used inside the loop are eager loaded using with()."
                    )

                if "DB::" in window or "::where(" in window or "->where(" in window:
                    findings.append(
                        f"- Query inside loop risk in {file.relative_to(project)} around line {i}\n"
                        f"  Advice: Move query outside loop or eager load/group data first."
                    )

    if not findings:
        return "N+1 QUERY DETECTOR — PHASE 242\nNo obvious N+1 risks found."

    return "N+1 QUERY DETECTOR — PHASE 242\n\n" + "\n".join(findings[:100])


def eloquent_optimization_advisor():
    project, error = _project()
    if error:
        return error

    findings = []

    for file in _php_files(project):
        text = _read(file)

        if "::all()" in text:
            findings.append(f"- {file.relative_to(project)} uses ::all(). Consider pagination, select(), or constrained queries.")

        if "->get()" in text and "paginate(" not in text and "limit(" not in text:
            findings.append(f"- {file.relative_to(project)} uses get(). Check if large result sets need pagination or limits.")

        if "count(" in text and "->get()" in text:
            findings.append(f"- {file.relative_to(project)} may count after fetching data. Prefer ->count() at database level.")

        if "->with(" not in text and re.search(r"return\s+view\(", text):
            findings.append(f"- {file.relative_to(project)} returns views. Check whether related models should be eager loaded with with().")

        if "select(" not in text and ("::query()" in text or "::where(" in text):
            findings.append(f"- {file.relative_to(project)} may fetch full columns. Consider select() for heavy tables.")

    if not findings:
        return "ELOQUENT OPTIMIZATION ADVISOR — PHASE 243\nNo obvious Eloquent optimization issues found."

    return "ELOQUENT OPTIMIZATION ADVISOR — PHASE 243\n\n" + "\n".join(findings[:120])


def database_index_suggestion_engine():
    project, error = _project()
    if error:
        return error

    columns = defaultdict(set)
    suggestions = []

    for file in _php_files(project):
        text = _read(file)

        for match in re.findall(r"->where\(['\"]([^'\"]+)['\"]", text):
            columns[match].add(str(file.relative_to(project)))

        for match in re.findall(r"->orderBy\(['\"]([^'\"]+)['\"]", text):
            columns[match].add(str(file.relative_to(project)))

        for match in re.findall(r"->join\(['\"][^'\"]+['\"],\s*['\"]([^'\"]+)['\"]", text):
            columns[match.split(".")[-1]].add(str(file.relative_to(project)))

    common_index_candidates = {
        "user_id", "company_id", "tenant_id", "customer_id", "product_id",
        "category_id", "supplier_id", "status", "slug", "email",
        "created_at", "updated_at", "deleted_at"
    }

    for column, files in sorted(columns.items()):
        confidence = "medium"
        if column in common_index_candidates or column.endswith("_id"):
            confidence = "high"

        suggestions.append(
            f"- Column: {column}\n"
            f"  Confidence: {confidence}\n"
            f"  Seen in: {', '.join(list(files)[:5])}\n"
            f"  Suggested migration line: $table->index('{column}');"
        )

    if not suggestions:
        return "DATABASE INDEX SUGGESTION ENGINE — PHASE 244\nNo obvious index candidates found."

    return "DATABASE INDEX SUGGESTION ENGINE — PHASE 244\n\n" + "\n\n".join(suggestions[:80])


def migration_rollback_simulator():
    project, error = _project()
    if error:
        return error

    migrations = project / "database" / "migrations"
    if not migrations.exists():
        return "MIGRATION ROLLBACK SIMULATOR — PHASE 245\ndatabase/migrations folder not found."

    findings = []

    for file in sorted(migrations.glob("*.php")):
        text = _read(file)

        up_match = re.search(r"function\s+up\s*\(.*?\)\s*:\s*void\s*{(.*?)}\s*public\s+function\s+down", text, re.DOTALL)
        down_match = re.search(r"function\s+down\s*\(.*?\)\s*:\s*void\s*{(.*?)}", text, re.DOTALL)

        down_body = down_match.group(1) if down_match else ""

        risk = []

        if "Schema::create" in text and "Schema::dropIfExists" not in down_body:
            risk.append("Creates table but down() may not drop it.")

        if "Schema::table" in text and "dropColumn" not in down_body and "dropForeign" not in down_body and "dropIndex" not in down_body:
            risk.append("Alters table but down() may not reverse columns/indexes/foreign keys.")

        if not down_body.strip():
            risk.append("Empty or missing down() method.")

        if risk:
            findings.append(
                f"- {file.name}\n  " + "\n  ".join(risk)
            )

    if not findings:
        return "MIGRATION ROLLBACK SIMULATOR — PHASE 245\nRollback structure looks acceptable from static inspection."

    return "MIGRATION ROLLBACK SIMULATOR — PHASE 245\n\n" + "\n\n".join(findings[:80])


def seeder_verification_system():
    project, error = _project()
    if error:
        return error

    seeders = project / "database" / "seeders"
    if not seeders.exists():
        return "SEEDER VERIFICATION SYSTEM — PHASE 246\ndatabase/seeders folder not found."

    findings = []

    for file in seeders.glob("*.php"):
        text = _read(file)

        if "truncate(" in text or "delete()" in text:
            findings.append(f"- {file.name}: destructive operation found. Must require manual confirmation.")

        if "firstOrCreate" not in text and "updateOrCreate" not in text and "insert(" in text:
            findings.append(f"- {file.name}: uses insert(). Consider idempotent seeders using firstOrCreate/updateOrCreate.")

        if "User::create" in text and "password" in text:
            findings.append(f"- {file.name}: creates users. Verify password hashing and avoid hardcoded production credentials.")

    if not findings:
        return "SEEDER VERIFICATION SYSTEM — PHASE 246\nSeeder files look safe from static inspection."

    return "SEEDER VERIFICATION SYSTEM — PHASE 246\n\n" + "\n".join(findings[:100])


def database_backup_assistant():
    project, error = _project()
    if error:
        return error

    env = project / ".env"
    if not env.exists():
        return "DATABASE BACKUP ASSISTANT — PHASE 247\n.env not found."

    text = _read(env)

    def env_value(key):
        match = re.search(rf"^{key}=(.*)$", text, re.MULTILINE)
        return match.group(1).strip().strip('"').strip("'") if match else ""

    db = env_value("DB_DATABASE")
    user = env_value("DB_USERNAME")
    host = env_value("DB_HOST") or "127.0.0.1"

    if not db or not user:
        return "DATABASE BACKUP ASSISTANT — PHASE 247\nDB_DATABASE or DB_USERNAME missing in .env."

    return f"""DATABASE BACKUP ASSISTANT — PHASE 247

Read-only mode. No backup was created.

Detected:
- Host: {host}
- Database: {db}
- Username: {user}
- Password: hidden

Safe backup command template:
mysqldump -h {host} -u {user} -p {db} > storage/backups/{db}_YYYYMMDD_HHMMSS.sql

Safety:
- JARVIS should not run mysqldump automatically yet.
- Add confirm-before-execute in a future phase.
- Never print DB_PASSWORD.
"""


def schema_visualization_engine():
    project, error = _project()
    if error:
        return error

    migrations = project / "database" / "migrations"
    if not migrations.exists():
        return "SCHEMA VISUALIZATION ENGINE — PHASE 248\ndatabase/migrations folder not found."

    tables = defaultdict(list)

    for file in sorted(migrations.glob("*.php")):
        text = _read(file)

        create_matches = re.findall(r"Schema::create\(['\"]([^'\"]+)['\"].*?function\s*\(Blueprint\s+\$table\)\s*{(.*?)}\s*\);", text, re.DOTALL)

        for table, body in create_matches:
            columns = re.findall(r"\$table->(\w+)\(['\"]([^'\"]+)['\"]", body)
            for col_type, col_name in columns:
                tables[table].append((col_name, col_type))

    if not tables:
        return "SCHEMA VISUALIZATION ENGINE — PHASE 248\nNo tables detected from migrations."

    lines = ["SCHEMA VISUALIZATION ENGINE — PHASE 248"]

    for table, cols in tables.items():
        lines.append(f"\nTABLE: {table}")
        for col_name, col_type in cols:
            lines.append(f"  - {col_name}: {col_type}")

    return "\n".join(lines[:500])


def er_diagram_generator():
    project, error = _project()
    if error:
        return error

    migrations = project / "database" / "migrations"
    if not migrations.exists():
        return "ER DIAGRAM GENERATOR — PHASE 249\ndatabase/migrations folder not found."

    tables = set()
    relationships = []

    for file in sorted(migrations.glob("*.php")):
        text = _read(file)

        for table in re.findall(r"Schema::create\(['\"]([^'\"]+)['\"]", text):
            tables.add(table)

        foreign_ids = re.findall(r"\$table->foreignId\(['\"]([^'\"]+)['\"]\)->constrained\(?['\"]?([^'\"\)]*)", text)

        for column, target in foreign_ids:
            source_guess = file.name.split("_create_")[-1].split("_table")[0]
            target_table = target or column.replace("_id", "s")
            relationships.append((source_guess, target_table, column))

    lines = ["ER DIAGRAM GENERATOR — PHASE 249", "", "Mermaid ER diagram:", "", "```mermaid", "erDiagram"]

    for table in sorted(tables):
        lines.append(f"    {table} {{")
        lines.append("        int id")
        lines.append("    }")

    for source, target, column in relationships:
        lines.append(f"    {target} ||--o{{ {source} : \"{column}\"")

    lines.append("```")

    return "\n".join(lines)


def api_documentation_generator():
    project, error = _project()
    if error:
        return error

    routes = project / "routes"
    if not routes.exists():
        return "API DOCUMENTATION GENERATOR — PHASE 250\nroutes folder not found."

    docs = ["API DOCUMENTATION GENERATOR — PHASE 250"]

    route_pattern = re.compile(
        r"Route::(get|post|put|patch|delete|apiResource|resource)\((.*?)\);",
        re.DOTALL
    )

    for route_file in routes.glob("*.php"):
        text = _read(route_file)
        matches = route_pattern.findall(text)

        if matches:
            docs.append(f"\nFILE: {route_file.relative_to(project)}")

        for method, body in matches:
            clean = " ".join(body.split())
            docs.append(f"- {method.upper()} {clean}")

    if len(docs) == 1:
        return "API DOCUMENTATION GENERATOR — PHASE 250\nNo routes detected."

    docs.append("\nNote: This is static route documentation. Dynamic middleware/auth/request validation inspection can be added later.")

    return "\n".join(docs[:500])
