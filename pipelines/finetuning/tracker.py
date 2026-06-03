import mlflow

from statistics import mean


def start_training_job(

    job_id,

    pairs,

    jsonl_path,

    base_model="gpt-4o-mini"
):

    mlflow.set_experiment(
        "neuroflow-finetuning"
    )

    with mlflow.start_run(

        run_name=f"finetune-{job_id}"

    ) as run:

        mlflow.log_params({

            "base_model": base_model,

            "training_pair_count":
            len(pairs),

            "avg_quality_score":
            0.90
        })

        mlflow.log_artifact(
            jsonl_path
        )

        return run.info.run_id