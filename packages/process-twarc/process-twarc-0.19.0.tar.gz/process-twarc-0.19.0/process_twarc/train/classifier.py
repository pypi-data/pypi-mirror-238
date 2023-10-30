
from transformers import AutoModelForSequenceClassification
from process_twarc.util import  load_dict
from process_twarc.train.util import  init_run, complete_trial, launch_study


def run_study(
    data_dir:str,
    path_to_config: str,
    path_to_storage: str,
    preprocessed_data: bool=False,
    group: str="",
    n_trials: int=100,
    should_prune: bool=False,
):
    
    def objective(trial):
        parameters, paths, trainer, stop_epoch = init_run(
            trial, 
            config,
            AutoModelForSequenceClassification,
            datasets,
            tokenizer,
            group=group,
            should_prune=should_prune
            )

        trainer.train()

        results = complete_trial(
            trainer,
            datasets,
            parameters,
            paths
        )
        return results

    config = load_dict(path_to_config) 
    tokenizer, datasets, study= launch_study(
        config,
        path_to_storage,
        data_dir,
        preprocessed_data,
        group=group
    )
    study.optimize(objective, n_trials=n_trials)