import json
import typing
from pathlib import Path
from typing import Any

import typer
from validio_sdk import ValidioError, dbt, util
from validio_sdk.graphql_client.input_types import DbtArtifactUploadInput

from validio_cli import AsyncTyper, ConfigDir, Namespace, get_client_and_config
from validio_cli.bin.entities import credentials

app = AsyncTyper(help="dbt related commands")


@app.async_command(help="Upload dbt artifact")
async def upload(
    config_dir: str = ConfigDir,
    namespace: str = Namespace(),
    credential_id: str = typer.Option(..., help="Credential name or ID"),
    manifest: Path = typer.Option(..., help="Path to the manifest file"),
    run_results: Path = typer.Option(help="Path to the run results file", default=None),
) -> None:
    vc, cfg = await get_client_and_config(config_dir)

    resolved_credential_id = await credentials.get_credential_id(
        vc, cfg, credential_id, namespace
    )
    if resolved_credential_id is None:
        raise ValidioError(f"Credential '{credential_id}' not found")

    try:
        manifest_content = util.read_json_file(manifest)
        trimmed_manifest = dbt.trim_manifest_json(
            typing.cast(dict[str, Any], manifest_content)
        )
    except Exception as e:
        raise ValidioError(f"Failed to process manifest file: {e}")

    run_results_content = None
    if run_results is not None:
        run_results_content = json.dumps(util.read_json_file(run_results))

    await vc.dbt_artifact_upload(
        input=DbtArtifactUploadInput(
            credential_id=resolved_credential_id,
            manifest=json.dumps(trimmed_manifest),
            run_results=run_results_content,
        )
    )
    return print("dbt artifact uploaded successfully")


if __name__ == "__main__":
    typer.run(app())
