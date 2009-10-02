##############################################################################
#
# Copyright (c) 2009 The MadGraph Development team and Contributors
#
# This file is a part of the MadGraph 5 project, an application which 
# automatically generates Feynman diagrams and matrix elements for arbitrary
# high-energy processes in the Standard Model and beyond.
#
# It is subject to the MadGraph license which should accompany this 
# distribution.
#
# For more information, please visit: http://madgraph.phys.ucl.ac.be
#
##############################################################################

"""A user friendly command line interface to access MadGraph features."""

import cmd
import sys
import os

import madgraph.iolibs.misc as misc
import madgraph.iolibs.import_v4 as import_v4

class MadGraphCmd(cmd.Cmd):
    """The command line processor of MadGraph"""

    def split_arg(self, line):
        """Split a line of arguments"""
        args = line.split()
        for arg in args:
            arg = arg.strip()
        return args

    def preloop(self):
        """Initializing before starting the main loop"""

        self.prompt = 'mg5>'

        # If possible, build an info line with current version number and date, from
        # the VERSION text file

        info = misc.get_pkg_info()
        info_line = ""

        if info.has_key('version') and  info.has_key('date'):
            len_version = len(info['version'])
            len_date = len(info['date'])
            if len_version + len_date < 30:
                info_line = "*         VERSION %s %s %s         *\n" % \
                            (info['version'],
                            (30 - len_version - len_date) * ' ',
                            info['date'])

        self.intro = "************************************************************\n" + \
                "*                                                          *\n" + \
                "*          W E L C O M E  to  M A D G R A P H  5           *\n" + \
                "*                                                          *\n" + \
                info_line + \
                "*                                                          *\n" + \
                "*    The MadGraph Development Team - Please visit us at    *\n" + \
                "*              https://launchpad.net/madgraph5             *\n" + \
                "*                                                          *\n" + \
                "*               Type 'help' for in-line help.              *\n" + \
                "*                                                          *\n" + \
                "************************************************************"

    # Import files

    def do_import(self, line):
        """Import files with external formats"""

        args = self.split_arg(line)

        if len(args) != 2:
            self.help_import()
            return False

        if args[0] is 'v4':

            #Try to guess which function to call according to the given path

            if os.path.isdir(args[1]):
                pass
            elif os.path.isfile(args[1]):
                filename = os.path.basename(args[1])
            else:
                print "Path %s is not valid" % args[1]


    # Access to shell
    def do_shell(self, line):
        "Run a shell command"

        if line.strip() is '':
            self.help_shell()
        else:
            print "running shell command:", line
            print os.popen(line).read(),

    # Various ways to quit
    def do_quit(self, line):
        sys.exit(1)

    def do_EOF(self, line):
        sys.exit(1)

    # In-line help

    def help_import(self):
        print "syntax: import (v4|...) FILENAME",
        print "-- imports files in various formats"

    def help_shell(self):
        print "syntax: shell CMD",
        print "-- run the shell command CMD and catch output"

    def help_quit(self):
        print "syntax: quit",
        print "-- terminates the application"

    def help_help(self):
        print "syntax: help",
        print "-- access to the in-line help"

if __name__ == '__main__':
    MadGraphCmd().cmdloop()
