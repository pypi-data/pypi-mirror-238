from pathlib import Path

import typer

import process as study_


app = typer.Typer(name="spike2py_reflex", help="Extract evoked responses from Spike2 data.")


@app.command()
def section(
    subject_id: str, study_path: str, trial_name: str, section_name: str, plot: bool = False
):
    """Extract reflexes from a given a section.

    Requires that the proper study file-folder structure be in place
    and that the study_info.json and study_reflex.json be present
    in the `study_path`. Note that a subject_reflex.json file is present
    in the subject folder it will be used and override study-level
    parameters. Similarly, if a section-specific json file is present in the
    subject's `proc` folder, it will be used and override study-level and
    subject-level parameters (e.g. <trial_name>_<section_name>_reflex.json).

    trial_info_json: Path to json file containing details required by spike2py.trial.TrialInfo

    Parameters
    ----------
    subject_id: Subject id that matches the folder name for the study.
    study_path: path to study folder.
    trial_name: Name of the trial containing section to be analysed
    section_name: Name of the section to analyssed.
    plot: Flag to indicate whether to generate and save figures.

    """
    reflex_study_info = study_.get_reflex_study_info(study_path)
    reflex_subject_info = subject_.get_reflex_subject_info(subject_id, reflex_study_info)
    section_.process(reflex_subject_info, trial_name, section_name, plot)


@app.command()
def subject(subject_id: str, study_path: str, plot: bool = False):
    """Extract reflexes from all sections of each trials for a given subject.

    Requires that the proper study file-folder structure be in place
    and that the study_info.json and study_reflex.json be present
    in the `study_path`. Also, a subject_reflex.json file can be present
    to override study-specific details.

    Parameters
    ----------
    subject_id: Subject id that matches the folder name for the study.
    study_path: path to study folder.
    plot: Flag to indicate whether to generate and save figures.
    """
    pass

@app.command()
def study(study_path: str, plot: bool = False):
    """Extract reflexes from all sections of each trials from all subjects for a study.

    Parameters
    ----------
    study_path: Path to study folder.
    plot: Flag to indicate whether to generate and save figures.
    """
    study_.process(Path(study_path), plot=plot)


if __name__ == "__main__":
    app()
