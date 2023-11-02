import spike2py_reflex as s2pr


def extract(info, data):
    """Extract reflexes for all muscles (emg) in section.

    Parameters
    ----------
    info: s2pr.Info
      Contains details about all aspects of the study and its processing
    data: spike2py.trial.Trial
      Data of trial section being analysed

    Returns
    -------
    s2pr.SectionReflexes, which contains the reflexes and supplementary details
    of the current setion.
    """
    stim_intensities = s2pr.utils.get_stim_intensity(info, data)
    extracted = dict()

    for emg_name in info.channels.emg:
        emg = getattr(data, emg_name)
        muscle_reflexes = dict()
        # specify sampling frequency to trigger computation of idx
        info.windows.fs = emg.info.sampling_frequency
        if info.triggers.type in [s2pr.utils.SINGLE, s2pr.utils.TRAIN]:
            muscle_reflexes = _extract_single_reflexes(
                emg_name, emg, stim_intensities, info
            )
        elif info.triggers.type == s2pr.utils.DOUBLE:
            muscle_reflexes = _extract_double_reflexes(
                emg_name, emg, stim_intensities, info
            )
        extracted[emg_name] = muscle_reflexes

    return s2pr.reflexes.SectionReflexes(info, extracted)


def _extract_single_reflexes(emg_name, emg, stim_intensities, info):
    """Extract reflexes from single or train stimulation"""

    extract_idxs = _get_extract_idx_singles(info)
    x_axis = _get_x_axis(info)
    reflexes = _get_single_reflexes(extract_idxs, stim_intensities, emg)

    muscle_reflexes = s2pr.reflexes.Singles(
        x_axis_extract=x_axis,
        reflexes=reflexes,
        type=info.triggers.type,
        sd_window_idx=info.windows.idx_sd,
        sd_window_ms=info.windows.ms_sd,
        reflex_windows_idx=info.windows.idx_reflexes[emg_name],
        reflex_windows_ms=info.windows.ms_reflexes[emg_name],
    )
    return muscle_reflexes


def _get_extract_idx_singles(info):
    """Get idx of each window from which to extract single reflexes"""
    extract_idxs = list()
    trigger_type = s2pr.utils.SINGLE
    if info.triggers.type == s2pr.utils.TRAIN:
        trigger_type = s2pr.utils.TRAIN_SINGLE_PULSE
    extract_idx = getattr(info.windows.idx_extract, trigger_type)
    for trigger_idx in info.triggers.extract:
        extract_idxs.append(_get_window(trigger_idx, extract_idx))
    if _start_of_first_window_out_of_bounds(extract_idxs):
        extract_idxs.pop(0)
    return extract_idxs


def _get_window(trigger_idx, window_idx):
    """Get a pair of idx values to extract reflex from a trigger"""
    if trigger_idx is None:
        return [None, None]
    # TODO: Presumably window_idx[0] is negative? If so, make note here
    lower = trigger_idx + window_idx[0]
    upper = trigger_idx + window_idx[1]
    return [lower, upper]


def _start_of_first_window_out_of_bounds(extract_idxs):
    return extract_idxs[0][0] < 0


def _get_x_axis(info):
    x_axis = list()
    if info.triggers.type == s2pr.utils.SINGLE:
        x_axis = info.windows.x_axes.single
    elif info.triggers.type == s2pr.utils.TRAIN:
        x_axis = info.windows.x_axes.train_single_pulse
    return x_axis


def _get_single_reflexes(extract_idxs: list, stim_intensities: list, emg):
    """
    Extract reflexes based on window idx for each trigger

    Parameters
    ----------
    extract_idxs: pairs of indexes for each reflex to extract
    stim_intensities: Intensities associated with each reflex (if stim intensity recorded)
    emg: spike2py data for given emg channel from which to extract reflexes

    Returns
    -------
    all extracted reflexes

    """
    reflexes = list()
    for (idx1_extract, idx2_extract), intensity in zip(
            extract_idxs, stim_intensities
    ):
        try:
            reflexes.append(
                s2pr.reflexes.Single(
                    waveform=emg.values[idx1_extract:idx2_extract],
                    extract_times=(emg.times[idx1_extract], emg.times[idx2_extract]),
                    extract_indexes=(idx1_extract, idx2_extract),
                    stim_intensity=intensity,
                )
            )
        except IndexError:
            print(f'Dropped a reflex asking for idx1 {idx1_extract} and idx2 {idx2_extract},'
                  f'from signal with length {len(emg.times)}')
    return reflexes


def _extract_double_reflexes(emg_name, emg, stim_intensities, info):
    """Extract reflexes from doubles"""

    trigger_windows = _get_extract_idx_doubles(info)
    reflexes = _get_double_reflexes(info, trigger_windows, stim_intensities, emg)

    muscle_reflexes = s2pr.reflexes.Doubles(
        x_axis_extract=info.windows.x_axes.double,
        x_axis_singles=info.windows.x_axes.double_single_pulse,
        reflexes=reflexes,
        type=info.triggers.type,
        sd_window_idx=info.windows.idx_sd,
        sd_window_ms=info.windows.ms_sd,
        reflex_windows_idx=info.windows.idx_reflexes[emg_name],
        reflex_windows_ms=info.windows.ms_reflexes[emg_name],
    )
    return muscle_reflexes


def _get_extract_idx_doubles(info) -> list:
    """Get windows to extract double, and each reflex individually

    Returns
    -------

    List of lists. Each item in list represents one double. For each of these, there are three pairs of indexes.
    These are to extract 1) the entire double, 2) the first reflex, and 3) the second reflex.

    e.g. [[extract_start, extract_end], [reflex1_start, reflex1_end], [reflex2_start, reflex2_end]] , ...]
    """
    extract_idxs = list()
    extract_idx = getattr(info.windows.idx_extract, info.triggers.type)
    double_idx = getattr(info.windows.idx_extract, "double_single_pulse")
    for trigger_idx_extract, trigger_idx_double in zip(
        info.triggers.extract, info.triggers.double
    ):
        extract = _get_window(trigger_idx_extract, extract_idx)
        reflex1 = _get_window(trigger_idx_double[0], double_idx)
        reflex2 = _get_window(trigger_idx_double[1], double_idx)
        extract_idxs.append([extract, reflex1, reflex2])
    return extract_idxs


def _get_double_reflexes(info, trigger_windows, stim_intensities, emg):
    reflexes = list()
    stim_intensities_second_pulse_doubles_removed = _remove_second_pulse(
        stim_intensities,
        info.triggers._triggers,
        info.windows.double_isi
    )
    for (
            (idx1_extract, idx2_extract),
            (idx1_reflex1, idx2_reflex1),
            (idx1_reflex2, idx2_reflex2),
    ), (intensity) in zip(trigger_windows, stim_intensities_second_pulse_doubles_removed):

        reflex1 = s2pr.reflexes.Single(waveform=emg.values[idx1_reflex1:idx2_reflex1],
                                       extract_indexes=(idx1_reflex1, idx2_reflex1),
                                       extract_times=(emg.times[idx1_reflex1], emg.times[idx2_reflex1]),
                                       )

        reflex2 = None
        if idx1_reflex2 is not None:
            reflex2 = s2pr.reflexes.Single(
                waveform=emg.values[idx1_reflex2:idx2_reflex2],
                extract_indexes=(idx1_reflex2, idx2_reflex2),
                extract_times=(emg.times[idx1_reflex2], emg.times[idx2_reflex2])
            )
        double = s2pr.reflexes.Double(
            waveform=emg.values[idx1_extract:idx2_extract],
            reflex1=reflex1,
            reflex2=reflex2,
            stim_intensity=intensity,
            extract_indexes=(idx1_extract, idx2_extract),
            extract_times=(emg.times[idx1_extract], emg.times[idx2_extract])
        )
        reflexes.append(double)

    return reflexes


# TODO: Add test that ensures that when doubles given, only first stim intensity retained
# TODO: Add test that ensures that when mix of singles and doubles, only first stim of double retained, plus all singles
def _remove_second_pulse(stim_intensities, triggers, double_isi):
    stim_intensities_second_pulse_doubles_removed = [stim_intensities[0]]
    for i in range(1, len(triggers)):
        isi = triggers[i] - triggers[i-1]
        if _pulse_not_second_in_double(isi, double_isi):
            stim_intensities_second_pulse_doubles_removed.append(stim_intensities[i])
    return stim_intensities_second_pulse_doubles_removed


def _pulse_not_second_in_double(isi, double_isi):
    return isi > (double_isi*s2pr.utils.CONVERT_MS_TO_S) * 1.05
