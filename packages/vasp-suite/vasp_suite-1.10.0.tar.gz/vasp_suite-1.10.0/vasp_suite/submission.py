# Imports
import socket


class SubmissionWriter():
    def __init__(self, title, cores, vasp_type):
        self.title = title
        self.cores = cores
        self.vasp_type = vasp_type

    @property
    def hostname(self):
        hostname = socket.gethostname()
        if 'csf3' in hostname:
            return 'csf3'
        elif 'csf4' in hostname:
            return 'csf4'
        else:
            return 'csf3'

    @property
    def handle_cores_csf3(self):
        if self.cores < 32:
            return '#$ -pe smp.pe {}'.format(self.cores)
        else:
            return '#$ -pe mpi-24-ib.pe {}'.format(self.cores)

    @property
    def handle_nodes_csf4(self):
        if self.cores < 40:
            return '#SBATCH -p multicore'
        else:
            return '#SBATCH -p multinode'

    @property
    def handle_vasp_type(self):
        options = {
                'standard': 'vasp_std',
                'gamma': 'vasp_gam',
        }

        if self.hostname == 'csf3':
            return 'mpirun -np {} {}_par'.format(
                    self.cores, options[self.vasp_type])
        if self.hostname == 'csf4':
            return 'mpirun -np {} {}'.format(
                    self.cores, options[self.vasp_type])

    def write_csf3_header(self, FileObject):
        FileObject.write("#!/bin/bash --login\n")
        FileObject.write("#$ -cwd\n")
        FileObject.write('{}\n'.format(self.handle_cores_csf3))
        FileObject.write("#$ -N {}\n".format(self.title))

    def write_csf4_header(self, FileObject):
        FileObject.write("#!/bin/bash --login\n")
        FileObject.write("{}\n".format(self.handle_nodes_csf4))
        FileObject.write("#SBATCH -n {}\n".format(self.cores))
        FileObject.write("#SBATCH --job-name={}\n".format(self.title))

    def write_module_load(self, FileObject):
        if self.hostname == 'csf3':
            FileObject.write('module load apps/intel-19.1/vasp/5.4.4\n')
        elif self.hostname == 'csf4':
            FileObject.write('module load vasp/5.4.4-iomkl-2020.02\n')

    def write_body(self, FileObject):
        FileObject.write('echo "Started running at $(date)"\n')
        FileObject.write('{}\n'.format(self.handle_vasp_type))
        FileObject.write('echo "Finished running at $(date)"\n')

    def write_array_header_csf3(self, array_file, FileObject):
        with open(array_file, 'r') as f:
            t_max = len([line for line in f.readlines()])
        FileObject.write('#$ -t 1-{}\n'.format(t_max))
        FileObject.write('module load apps/intel-19.1/vasp/5.4.4\n\n')
        FileObject.write('TASK_ID=$SGE_TASK_ID\n')
        FileObject.write('STEM=$(sed -n "${{TASK_ID}}p" {})\n'.format(array_file))
        FileObject.write('export CurrDir=$(pwd -P)\n')

    def write_array_header_csf4(self, array_file, FileObject):
        with open(array_file, 'r') as f:
            t_max = len([line for line in f.readlines()])
        FileObject.write('#SBATCH -a 1-{}\n'.format(t_max))
        FileObject.write('module load vasp/5.4.4-iomkl-2020.02')
        FileObject.write('TASK_ID=$SLURM_ARRAY_TASK_ID\n')
        FileObject.write('STEM=$(sed -n "${{TASK_ID}}p" {})\n'.format(array_file))
        FileObject.write('export CurrDir=$(pwd -P)\n')

    def write_phonopy_body(self, FileObject):
        FileObject.write('echo "Started running at $(date)"\n')
        FileObject.write('if [ ! -d "$CurrDir/$STEM" ]; then\n')
        FileObject.write('\tmkdir $CurrDir/$STEM\n')
        FileObject.write('fi\n\n')
        FileObject.write('mv $CurrDir/POSCAR-$STEM $CurrDir/$STEM/\n')
        FileObject.write('cp $CurrDir/INCAR $CurrDir/$STEM/\n')
        FileObject.write('cp $CurrDir/KPOINTS $CurrDir/$STEM/\n')
        FileObject.write('cp $CurrDir/POTCAR $CurrDir/$STEM/\n')
        FileObject.write('cd $CurrDir/$STEM/\n')
        FileObject.write('mv POSCAR-$STEM POSCAR\n')
        FileObject.write('{}\n'.format(self.handle_vasp_type))
        FileObject.write('cd $CurrDir\n\n')
        FileObject.write('echo "Finished running at $(date)"\n')

    def write_convergence_body(self, FileObject):
        FileObject.write('echo "Started running at $(date)"\n')
        FileObject.write('cd $CurrDir/$STEM\n')
        FileObject.write('{}\n'.format(self.handle_vasp_type))
        FileObject.write('cd $CurrDir\n\n')
        FileObject.write('echo "Finished running at $(date)"\n')
