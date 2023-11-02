"""
Handles the automation of phonopy calculations.
"""
import os


def store_disp_files():
    """
    Identifies the number of 'POSCAR-XXX' files in the current directory.
    """
    disp_files = [x for x in os.listdir()
                  if x.startswith('POSCAR-')]

    disp_files = [x.split('-')[1] for x in disp_files]
    print('Found {} displacement files'.format(len(disp_files)))
    disp_files = sorted(disp_files, key=int)

    with open('phonon_files.txt', 'w') as f:
        for i in disp_files:
            f.write('{}\n'.format(str(i)))


def check_config():
    """
    Checks if the config file exists.
    """
    if os.path.isfile(os.path.join(os.path.expanduser('~'),
                                   '.vasp_suite_configs/phonon.ini')):
        return True
    else:
        return False
