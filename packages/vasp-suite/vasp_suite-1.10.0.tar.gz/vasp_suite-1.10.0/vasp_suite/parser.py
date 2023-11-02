"""
A module for parsing vasp output files.
"""

import os
import re

from .structure import Structure


class Parser(Structure):
    """
    Parent class for all parsers
    """

    def __init__(self, output_file):
        """
        Initializes the parser object.
        """
        # Initialize the structure object
        if not (os.path.exists('POSCAR')
                or os.path.exists('CONTCAR')):
            raise IOError("No POSCAR or CONTCAR file found.")
        poscar = Structure.from_poscar('POSCAR')
        for atrr in poscar.__dict__:
            setattr(self, atrr, getattr(poscar, atrr))
        self.output_file = output_file

    @property
    def read_lines(self):
        """
        Reads the lines from the output file
        """
        with open(self.output_file, 'r') as f:
            return f.readlines()


class ParseOUTCAR(Parser):
    """
    Parses the OUTCAR file
    """

    # Patterns

    external_pressureREGEX = re.compile(
            r'^\s+external\s+pressure\s+=\s+(?P<pressure>[+-]?\d+\.\d+)\s+'
            )

    elapsed_timeREGEX = re.compile(
            r'^\s+Elapsed\s+time\s+\(sec\)\:\s+(?P<time>\d+\.\d+)\s+'
            )

    def __init__(self, output_file='OUTCAR'):
        """
        Initializes the OUTCAR parser object.
        """
        super().__init__(output_file)

    @property
    def external_pressure(self):
        """
        Returns the external pressure
        """
        # UNITS: kB
        for line in self.read_lines:
            match = self.external_pressureREGEX.match(line)

            if match:
                yield float(match.group('pressure'))

    @property
    def elapsed_time(self):
        for line in self.read_lines:
            match = self.elapsed_timeREGEX.match(line)

            if match:
                yield float(match.group('time'))


class ParseOSZICAR(Parser):
    """
    Parses the OSZICAR file
    """

    energyRegex = re.compile(
            r"^\s+\d+\s+F=\s+[+-]?(\d*)?\.\d*[eE]?[+-]?\d*\s+E0=\s+(?P<e_0>[+-]?(\d*)?\.\d*[eE]?[+-]?\d*)\s+"
            )

    stepREGEX = re.compile(
            r'[A-Z]{3}:\s+(?P<step>\d+)\s+'
            )

    def __init__(self, ouput_file='OSZICAR'):
        """
        Initializes the OSZICAR parser object.
        """
        super().__init__(ouput_file)

    @property
    def energy(self):
        """
        returns the energy per atom
        """
        for line in self.read_lines:
            match = self.energyRegex.match(line)

            if match:
                yield float(match.group('e_0'))

    @property
    def electronic_steps(self):
        """
        returns the number of electronic steps per
        ionic step
        """
        steps = []
        for line in self.read_lines:
            match = self.stepREGEX.match(line)

            if match:
                steps.append(int(match.group('step')))
        electronic_steps = []
        prev = 0
        for idx, step in enumerate(steps):
            if step == 1:
                electronic_steps.append(steps[prev:idx])
                prev = idx
        electronic_steps.append(steps[prev:])
        for list in electronic_steps:
            if len(list) < 1:
                electronic_steps.remove(list)
        return [max(x) for x in electronic_steps]
