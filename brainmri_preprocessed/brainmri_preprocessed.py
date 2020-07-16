#!/usr/bin/env python                                            
#
# brainmri_preprocessed ds ChRIS plugin app
#
# (c) 2016-2019 Fetal-Neonatal Neuroimaging & Developmental Science Center
#                   Boston Children's Hospital
#
#              http://childrenshospital.org/FNNDSC/
#                        dev@babyMRI.org
#


import  os
from    os          import listdir, sep
from    os.path     import abspath, basename, isdir
import  shutil
import  pudb
import  sys
import  time
import  glob
sys.path.append(os.path.dirname(__file__))

# import the Chris app superclass
from chrisapp.base import ChrisApp


Gstr_title = """

| |             (_)                    (_)                                                             | |
| |__  _ __ __ _ _ _ __  _ __ ___  _ __ _     _ __  _ __ ___ _ __  _ __ ___   ___ ___  ___ ___  ___  __| |
| '_ \| '__/ _` | | '_ \| '_ ` _ \| '__| |   | '_ \| '__/ _ \ '_ \| '__/ _ \ / __/ _ \/ __/ __|/ _ \/ _` |
| |_) | | | (_| | | | | | | | | | | |  | |   | |_) | | |  __/ |_) | | | (_) | (_|  __/\__ \__ \  __/ (_| |
|_.__/|_|  \__,_|_|_| |_|_| |_| |_|_|  |_|   | .__/|_|  \___| .__/|_|  \___/ \___\___||___/___/\___|\__,_|
                                       ______| |            | |                                           
                                      |______|_|            |_|                                           

"""

Gstr_synopsis = """



    NAME

       brainmri_preprocessed.py 

    SYNOPSIS

        python brainmri_preprocessed.py                                         \\
            [-h] [--help]                                               \\
            [--json]                                                    \\
            [--man]                                                     \\
            [--meta]                                                    \\
            [--savejson <DIR>]                                          \\
            [-v <level>] [--verbosity <level>]                          \\
            [--version]                                                 \\
            [--copySpec <copySpec>]                                     \\
            <inputDir>                                                  \\
            <outputDir> 

    BRIEF EXAMPLE

        * Bare bones execution

            mkdir in out && chmod 777 out
            python brainmri_preprocessed.py   \\
                                in    out

    DESCRIPTION

        `brainmri_preprocessed.py` ...

    ARGS

        [-h] [--help]
        If specified, show help message and exit.
        
        [--json]
        If specified, show json representation of app and exit.
        
        [--man]
        If specified, print (this) man page and exit.

        [--meta]
        If specified, print plugin meta data and exit.
        
        [--savejson <DIR>] 
        If specified, save json representation file to DIR and exit. 
        
        [-v <level>] [--verbosity <level>]
        Verbosity level for app. Not used currently.
        
        [--version]
        If specified, print version number and exit. 
        
        [-T <targetTreeHead>] | [--treePrint <targetTreeHead>]
        Print a simple directory tree rooted on <targetTreeHead>. Typically
        used to print the internal database with a 
        
                    -T ../preprocessed
                    
        [-c <copySpec>] | [--copySpec <copySpec>]
        A comma separated string denoting the preprocessed subdirs to copy. 
        Note that a substring glob is performed, thus a spec of 'input' will
        target 'input_data'.
        
        [-P <processDelay>] | [--processDelay <processDelay>]
        A delay timer to simulate remote processing. The script will pause for
        <processDelay> seconds.

"""


class Brainmri_preprocessed(ChrisApp):
    """
    A app to demonstrate the various results of GE pipeline.
    """
    AUTHORS                 = 'Sandip Samal (sandip.samal@childrens.harvard.edu)'
    SELFPATH                = os.path.dirname(os.path.abspath(__file__))
    SELFEXEC                = os.path.basename(__file__)
    EXECSHELL               = 'python3'
    TITLE                   = 'A ChRIS plugin that contains all the preprocessed output of different plug-ins inside the GE workflow'
    CATEGORY                = ''
    TYPE                    = 'ds'
    DESCRIPTION             = 'A app to demonstrate the various results of GE pipeline'
    DOCUMENTATION           = 'http://wiki'
    VERSION                 = '0.1'
    ICON                    = '' # url of an icon image
    LICENSE                 = 'Opensource (MIT)'
    MAX_NUMBER_OF_WORKERS   = 1  # Override with integer value
    MIN_NUMBER_OF_WORKERS   = 1  # Override with integer value
    MAX_CPU_LIMIT           = '' # Override with millicore value as string, e.g. '2000m'
    MIN_CPU_LIMIT           = '' # Override with millicore value as string, e.g. '2000m'
    MAX_MEMORY_LIMIT        = '' # Override with string, e.g. '1Gi', '2000Mi'
    MIN_MEMORY_LIMIT        = '' # Override with string, e.g. '1Gi', '2000Mi'
    MIN_GPU_LIMIT           = 0  # Override with the minimum number of GPUs, as an integer, for your plugin
    MAX_GPU_LIMIT           = 0  # Override with the maximum number of GPUs, as an integer, for your plugin

    # Use this dictionary structure to provide key-value output descriptive information
    # that may be useful for the next downstream plugin. For example:
    #
    # {
    #   "finalOutputFile":  "final/file.out",
    #   "viewer":           "genericTextViewer",
    # }
    #
    # The above dictionary is saved when plugin is called with a ``--saveoutputmeta``
    # flag. Note also that all file paths are relative to the system specified
    # output directory.
    OUTPUT_META_DICT = {}
    
    str_tree                = ''

    @staticmethod
    def dirTree_probe(dir, padding, print_files=False):
        """
        Simple method that returns a string of a dir tree layout. 
        Relies on global variable, <str_tree>!!!
        """
        Brainmri_preprocessed.str_tree += padding[:-1] + '+-' + basename(abspath(dir)) + '/' + '\n'
        padding = padding + ' '
        files = []
        if print_files:
            files = listdir(dir)
        else:
            files = [x for x in listdir(dir) if isdir(dir + sep + x)]
        count = 0
        for file in files:
            count += 1
            Brainmri_preprocessed.str_tree += padding + '|' + '\n'
            path = dir + sep + file
            if isdir(path):
                if count == len(files):
                    Brainmri_preprocessed.dirTree_probe(path, padding + ' ', print_files)
                else:
                    Brainmri_preprocessed.dirTree_probe(path, padding + '|', print_files)
            else:
                Brainmri_preprocessed.str_tree += padding + '+-' + file + '\n'
        return Brainmri_preprocessed.str_tree

    def define_parameters(self):
        """
        Define the CLI arguments accepted by this plugin app.
        Use self.add_argument to specify a new app argument.
        """
        self.add_argument("-T", "--treePrint",
                            help        = "Simple dirtree print. Specify head of target tree",
                            type        = str,
                            dest        = 'treePrint',
                            optional    = True,
                            default     = "")
        self.add_argument("-c", "--copySpec",
                            help        = "A comma separated string denoting the subdirs to copy",
                            type        = str,
                            dest        = 'copySpec',
                            optional    = True,
                            default     = "")
        self.add_argument("-P", "--processDelay",
                            help        = "delay timer to simulate remote processing",
                            type        = str,
                            dest        = 'processDelay',
                            optional    = True,
                            default     = "0")
        self.add_argument("--jsonReturn",
                            help        = "output final return in json",
                            type        = bool,
                            dest        = 'jsonReturn',
                            action      = 'store_true',
                            optional    = True,
                            default     = False)


    def run(self, options):
        """
        Define the code to be run by this plugin app.
        """
        if len(options.treePrint):
            str_tree = ''
            str_tree = Brainmri_preprocessed.dirTree_probe(options.treePrint, '')
            print(str_tree)
            sys.exit(0)

        print(Gstr_title)
        print('Version: %s' % Brainmri_preprocessed.VERSION)

        if len(options.processDelay):
            print('Simulating a process delay of %s seconds...' % options.processDelay)
            time.sleep(int(options.processDelay))
            
        str_all_dirs = '../preprocessed'           

        

        # pudb.set_trace()
        if options.copySpec == "":
            lstr_targetDir = os.listdir(str_all_dirs)
        else:
            lstr_targetDir  = options.copySpec.split(',')
            
        lstr_targetDirFull   = os.listdir(options.outputdir)
        if len(lstr_targetDirFull):
            for present_dir in lstr_targetDirFull: 
                print('Deleting any pre-existing data in output dir: %s...' % present_dir)
                shutil.rmtree('%s' % (options.outputdir + "/"+present_dir), ignore_errors = True)
        
        for str_targetDir in lstr_targetDir:
            lstr_sourceDir   = glob.glob('%s/*%s*' % ( str_all_dirs,str_targetDir))
            if len(lstr_sourceDir):
                str_targetDirFull   = '%s/%s' % \
                    (options.outputdir, os.path.basename(lstr_sourceDir[0]))
                if os.path.isdir(lstr_sourceDir[0]):
                    print('Copying tree from %s to %s...' % \
                        (lstr_sourceDir[0], str_targetDirFull))
                    shutil.copytree(lstr_sourceDir[0], str_targetDirFull,dirs_exist_ok=True)


    def show_man_page(self):
        """
        Print the app's man page.
        """
        print(Gstr_synopsis)


# ENTRYPOINT
if __name__ == "__main__":
    chris_app = Brainmri_preprocessed()
    chris_app.launch()
