from pathlib import Path
import pickle
import spike2py_preprocess as s2pp
import spike2py_reflex as s2pr


def study(study_path: Path):
    """Extract reflexes for all trials of all subject for a study

    Parameters
    ----------
    study_path: Path to study folder. Folder is to be structured as indicated in spike2py_preprocess docs
    """
    info = s2pr.info.Info(study_path)
    for subject_ in info.subjects:
        subject(subject_, study_path=study_path)


def subject(subject_: str, study_path: Path):
    """Process all trials and their sections for a given subject

    Parameters
    ----------
    subject_: Subject id, which also has to be the name of their folder
    study_path: Path to study folder
    info: Study-related details; required if called internally
    plot: Whether to generate plots

    """
    print(f"\tsubject: {subject_}")
    subject_folder = study_path / subject_ / "proc"
    for item in subject_folder.iterdir():
        if item.is_file():
            if item.stem.split("_")[-1] == "reflexes":
                print(f"\t\t plotting {item.stem}")
                with open(item, "rb") as f:
                    section = pickle.load(f)

                s2pr.plot.reflexes(section)
                s2pr.plot.outcomes(section)

    subject_path_reflexes = study_path / subject_ / "figures" / "reflexes"
    s2pp.utils.merge_pdfs(subject_path_reflexes)

    subject_path_outcomes = study_path / subject_ / "figures" / "outcomes"
    s2pp.utils.merge_pdfs(subject_path_outcomes)
