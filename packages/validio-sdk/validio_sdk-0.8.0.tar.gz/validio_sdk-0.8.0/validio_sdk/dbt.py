"""Utilities for dbt."""


def trim_manifest_json(manifest: dict) -> dict:
    """
    Takes a dbt manifest json and discards all the fields that are not relevant
    used by the validio platform.

    :param manifest: The manifest object
    """
    models, relevant_sources = _extract_sql_models(manifest)
    sources = _extract_sources(manifest, relevant_sources)
    return {
        "metadata": _extract_metadata(manifest),
        "nodes": models,
        "sources": sources,
    }


def _extract_metadata(manifest: dict) -> dict:
    if "metadata" not in manifest:
        return {}

    m = manifest["metadata"]
    trimmed = {}
    for f in [
        "dbt_schema_version",
        "dbt_version",
        "generated_at",
        "invocation_id",
        "project_name",
        "project_id",
        "user_id",
        "adapter_type",
    ]:
        if f in m:
            trimmed[f] = m[f]
    return trimmed


def _trim_model_column(column: dict) -> dict:
    trimmed = {}
    for f in ["name", "description"]:
        if f in column:
            trimmed[f] = column[f]
    return trimmed


def _extract_sql_models(manifest: dict) -> tuple[dict, set]:
    if "nodes" not in manifest:
        return {}, set({})

    relevant_sources = set({})
    models = {}
    for k, m in manifest["nodes"].items():
        if k.split(".")[0] != "model" or m["language"] != "sql":
            continue

        verbatim_fields = [
            "package_name",
            "database",
            "schema",
            "name",
            "description",
            "created_at",
            "relation_name",
            "compiled_code",
            "resource_type",
            "depends_on",
            "original_file_path",
            "unique_id",
            "config",
            "tags",
        ]
        trimmed = {}
        for f in verbatim_fields:
            if f in m and not (isinstance("str", type(m[f])) and not m[f]):
                trimmed[f] = m[f]

        if "config" in m:
            trimmed["config"] = {
                "materialized": m["config"]["materialized"],
            }

        if "columns" in m:
            trimmed_columns = _get_trimmed_columns(m)
            if len(trimmed_columns) > 0:
                trimmed["columns"] = trimmed_columns

        if (
            "depends_on" in m
            and "nodes" in m["depends_on"]
            and len(m["depends_on"]["nodes"]) > 0
        ):
            depends_on_nodes = m["depends_on"]["nodes"]
            for node_id in depends_on_nodes:
                if node_id.startswith("source"):
                    relevant_sources.add(node_id)

            trimmed["depends_on"] = {"nodes": depends_on_nodes}

        models[k] = trimmed

    return models, relevant_sources


def _get_trimmed_columns(manifest: dict) -> dict:
    trimmed_columns = {}
    for column_name, column_obj in manifest["columns"].items():
        trimmed_column = _trim_model_column(column_obj)
        if len(trimmed_column) > 0:
            trimmed_columns[column_name] = trimmed_column
    return trimmed_columns


def _extract_sources(manifest: dict, relevant_sources: set) -> dict:
    if "sources" not in manifest:
        return {}

    sources = {}
    for k, s in manifest["sources"].items():
        if k not in relevant_sources:
            continue

        fields = [
            "database",
            "schema",
            "name",
            "description",
            "created_at",
            "relation_name",
            "resource_type",
            "original_file_path",
            "package_name",
            "unique_id",
            "tags",
        ]
        trimmed = {}
        for f in fields:
            if f in s:
                if isinstance("str", type(s[f])) and not s[f]:
                    continue
                trimmed[f] = s[f]

        if len(trimmed) > 0:
            sources[k] = trimmed

    return sources
