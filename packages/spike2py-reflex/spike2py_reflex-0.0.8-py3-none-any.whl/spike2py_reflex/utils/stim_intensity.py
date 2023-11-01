import sys

from spike2py_preprocess.trial_sections import find_nearest_time_index
import spike2py_reflex as s2pr


def get_stim_intensity(info, data) -> list:
    ch = _get_stim_intensity_channel(info, data)
    intensities = list()
    for trigger in info.triggers._triggers:
        intensity_value = None
        if ch is not None:
            idx = find_nearest_time_index(ch.times, trigger)
            intensity_value = round(ch.values[idx])
        intensities.append(intensity_value)
    try:
        intensities = _verify_doubles_at_same_intensities(info, intensities, info.windows.double_isi)
    except AttributeError:
        pass
    return intensities


# TODO: add test where there is different stim intensities (Janie H-reflex trial S6 '1000us_bi_h')
# TODO: add test where there is different stim intensities for a double (Janie TSS trial S7 '400us_bi_tss_tss')


def _verify_doubles_at_same_intensities(info, intensities, double_isi):
    triggers = info.triggers._triggers
    for i, (trigger, intensity) in enumerate(zip(triggers, intensities)):
        if i == 0:
            previous_trigger_time = trigger
            previous_trigger_intensity = intensity
        current_trigger_time = trigger
        current_trigger_intensity = intensity
        isi = current_trigger_time - previous_trigger_time
        if isi < (double_isi*s2pr.utils.CONVERT_MS_TO_S) * 1.05:
            if previous_trigger_intensity != current_trigger_intensity:
                print('!' * 80,
                      f'\nIntensity of first and second trigger for double not equal.\n\n'
                      f'\t\tsubject: {info.subject}\n'
                      f'\t\ttrial: {info.trial}\n'
                      f'\t\tsection: {info.section}\n',
                      f'\t\ttrigger 1 time:{previous_trigger_time}\n',
                      f'\t\tstim intensity 1:{previous_trigger_intensity}\n',
                      f'\t\ttrigger 2 time:{current_trigger_time}\n',
                      f'\t\tstim intensity 2:{current_trigger_intensity}\n\n',
                      'To remove this double from the section, please add the window'
                      f'[{previous_trigger_time-0.2}, {current_trigger_time + 0.2}]\n'
                      f'to the subject trial json file under "rejected_trigger_windows"\n',
                      '!' * 80,
                      '\n')
                sys.exit(1)
    return intensities


def _get_stim_intensity_channel(info, data):
    stim_intensity = None
    try:
        stim_intensity = getattr(data, info.channels.stim_intensity)
    except AttributeError:
        print(f'\t\tstudy: {info.study}; '
              f'trial: {info.trial}; '
              f'section: {info.section} --> no `stim_intensity` channel.')
    return stim_intensity
