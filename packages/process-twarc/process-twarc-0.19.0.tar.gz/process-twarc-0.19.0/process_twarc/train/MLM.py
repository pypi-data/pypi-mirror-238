
from transformers import Trainer, AutoModelForMaskedLM
from process_twarc.util import  load_dict
from process_twarc.train.util import  init_run, reinit_run, check_if_complete, complete_trial, launch_study

def initiate_trial(
    data_dir:str,
    path_to_config: str,
    path_to_storage: str,
    override_parameters: dict={},
    group: str="",
    preprocessed_data: bool=True,
    pause_on_epoch: bool=False
):

    def objective(trial):
        parameters, paths, trainer, stop_epoch = init_run(
            trial, 
            config, 
            AutoModelForMaskedLM,
            datasets,
            tokenizer,
            group=group, 
            override_parameters=override_parameters, 
            pause_on_epoch=pause_on_epoch
            )
        
   
        trainer.train()
        complete = check_if_complete(trainer, parameters, stop_epoch)

        if complete:
            trial_value = complete_trial(
                trainer,
                datasets,
                parameters,
                paths
            )
        
        else:
            trial_value = 1
        
        return trial_value
    
    config = load_dict(path_to_config)
    tokenizer, datasets, study = launch_study(
        config,
        path_to_storage,
        data_dir,
        preprocessed_data,
        group=group
    )
    study.optimize(objective, n_trials=1)


def resume_trial(
    data_dir:str,
    path_to_config: str,
    trial_checkpoint: str,
    preprocessed_data: bool=True,
    pause_on_epoch: bool=False
):
    
    config = load_dict(path_to_config)
    paths, parameters, datasets, trainer, stop_epoch = reinit_run(
        trial_checkpoint, 
        config, 
        AutoModelForMaskedLM,
        data_dir,
        preprocessed_data=preprocessed_data,
        pause_on_epoch=pause_on_epoch
        )

    trainer.train(resume_from_checkpoint=paths["last_checkpoint"])
    complete = check_if_complete(trainer, parameters, stop_epoch)
    
    if complete:
        complete_trial(
            trainer, 
            datasets, 
            parameters,
            paths)
