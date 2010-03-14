#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2008, Ahmet Emre Aladag
# http://www.emrealadag.com
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.
#
# Please read the COPYING file.

from pre import *
from post import *
import sys

def help():
    print '''
    Usage:    python pyorainstaller.py [OPTION]
    Starts the pre-configuration process when used with no argument. 
        
        QuickStart commands:
        --pre-configuration         Starts the pre-configuration process up to start of runInstaller executable.
        --post-configuration        Starts the post-configuarion process to configure auto-starting instance and hostname.
      
        Manual Backup operations:
        --backup                    Backs up the conf and .bash_profile files meant to be modified throughout the
                                    configuration process.
        --restore                   Restores the conf and .bash_profile files which are backed up formerly.
        --rollback                  Does --restore command, additionally drops oracle user and groups, deletes ORACLE_BASE.
                                 
        Manual Stepping:
        --part1                     Starts the part1 process (pre-configuration except for extracting zip file.)
        --part2                     Starts the part2 process (extracts the zip file.)
        --part3                     Starts the part3 process (same as --post-configuration)        
        
    '''
    
    
    
    """
    'change_release', 'check_backup', 'check_config', 'check_package', 'configure_env_settings',
     'configure_hangcheck_timer', 'configure_kernel_parameters', 'configure_shell_limits',
      'create_dbora', 'create_installation_path', 'create_oracle_user_account', 'fix_dbstart',
       'flag_sid', 'help', 'link_dbora', 'part1', 'part2', 'part3', 'restore_backup',
        'rollback', 'set_ip', 'set_oracle_passwd', 'take_backup', 'unzip_the_setup_files'
    """
    
def main():
    if len(sys.argv)<2:
        help()
        sys.exit()
    option = sys.argv[1]
        
    action = {
              "--pre-configuration" : pre_configuration,
              "--post-configuration": post_configuration,
              
              "--backup"            : take_backup,
              "--restore"           : restore_backup,
              "--rollback"          : rollback,
              
              "--part1"             : part1,
              "--part2"             : part2,
              "--part3"             : part3,
              
              "--help"              : help,
              "-h"                  : help,
              }
    
    action[option]()

if __name__ == "__main__":
    main()