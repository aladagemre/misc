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

'''
Pre-configuration processes
'''
from config import *
from lib import *
import commands
import os
import shutil
import sys
import time



def part1():
    print "#----------------------------------------#"
    print "# Starting the Part 1 - Preconfiguration #"
    print "#                                        #"
    print "#----------------------------------------#"


    check_config()
    check_package()
    take_backup()
    change_release()
    create_oracle_user_account()
    set_oracle_passwd()
    create_installation_path()
    configure_kernel_parameters()
    configure_shell_limits()
    configure_hangcheck_timer()
    configure_env_settings()

def check_config():
    '''Checks the setup zip file existance and maybe some other configs in the future.'''
    
    if os.path.exists( ZIP_FILE_PATH ):
        print "The setup zip file found... OK!"
    else:
        print "The setup zip file could not be found!"
        sys.exit()

def check_package():
    """
    rpm -q binutils compat-db control-center gcc gcc-c++ glibc glibc-common gnome-libs libstdc++ libstdc++-devel make pdksh sysstat xscreensaver
    """
    command = "rpm -q libXp compat-libstdc++"
    output = commands.getoutput( command )
    if "not installed" in output:
        os.system( "rpm -i ./packages/libXp-1.0.0-2.2.i386.rpm ./packages/compat-libstdc++-8-3.3.4.2.i386.rpm" )


def check_backup():
    '''Checks if there's a ./backups directory with some files in it, then ask for confirmation.'''
    if os.path.exists( "./backups" ) and os.listdir( "./backups" ).__len__() > 0:
        print "Backup files exist. This operation will overwrite these files. Proceed anyway? [y/N] ", 
        choice = raw_input()
        if choice != "y":
            sys.exit( 0 )


def take_backup():
    '''Backs up the files to be modified throughout the pre-configuration process.'''
    
    check_backup()
    if not os.path.exists( "./backups" ):
        os.mkdir( "./backups" )
    
    for source_path in BACKUP_FILE_PATHS:
        destination_path = "./backups/%s" % os.path.basename( source_path )
        
        if os.path.exists( source_path ):
            shutil.copyfile( source_path, destination_path )
            print "Backed up the file %s" % source_path
        else:
            print "File %s could not be found, will not take backup of it!" % source_path      
                 
       

def restore_backup():
    '''Restores the taken backups to the system.'''

    for destination_path in BACKUP_FILE_PATHS:
        source_path = "./backups/%s" % os.path.basename( destination_path )
        
        if os.path.exists( source_path ):
            if os.path.exists( os.path.dirname( destination_path ) ):
                shutil.copyfile( source_path, destination_path )
                print "Restored the file %s" % destination_path
            else:
                os.mkdir( os.path.dirname( destination_path ) )
        else:
            print "The source file %s could not be found, will not restore it!" % source_path
                
    if os.path.exists( "./backups" ):
        shutil.rmtree( "./backups" )
    else:
        print "Could not find backup dir, not removing..."
        
def rollback():
    '''Restores the backups and deletes USER_ORACLE, GROUP_OINSTALL, GROUP_DBA, ORACLE_BASE directory,
    removes module hangcheck-timer from the kernel.
    '''
    restore_backup()
    
    command = \
'''
userdel -r %s
groupdel %s
groupdel %s
rmmod -s hangcheck-timer
'''% ( USER_ORACLE, GROUP_OINSTALL, GROUP_DBA )
    os.system( command )
    if os.path.exists( ORACLE_BASE ):
        shutil.rmtree( ORACLE_BASE )
    if os.path.exists( '%s/database' % TEMP_SETUP_FILES ):
	    choice = raw_input("Do you want to remove the extracted setup files?[y/N]")
	    if choice == "y":
		shutil.rmtree('%s/database' % TEMP_SETUP_FILES)
	    else:
		print "Leaving the extracted setup files undeleted ..."
		
		   
	    

def change_release():
    ''' Changes the RHEL release information to rhel4'''
    
    print "Changing the RHEL release to rhel4 ..."
    os.system( 'echo "rhel4" > /etc/redhat-release' )


def create_oracle_user_account():
    '''Creates the groups oinstall, dba and the user oracle belonging to them.'''
    
    print "Creating groups and the %s user ..." % USER_ORACLE
    command = \
'''/usr/sbin/groupadd %s
/usr/sbin/groupadd %s
/usr/sbin/useradd -m -g %s -G %s %s''' % ( GROUP_OINSTALL, GROUP_DBA, GROUP_OINSTALL, GROUP_DBA, USER_ORACLE )
    os.system( command )
    # Now we have to manually backup the bash_profile. Because it hadn't been created until now.
    shutil.copyfile( "/home/%s/.bash_profile" % USER_ORACLE, "./backups/.bash_profile" )
    
def set_oracle_passwd():
    '''Sets the user oracle's password'''
    
    print "Setting the password for the user %s ..." % USER_ORACLE
    command = '''passwd %s''' % ( USER_ORACLE )
    os.system( command )


def create_installation_path():
    '''Creates the oracle installation path'''
    
    print "Creating the installation path ..."
    command = \
'''mkdir -p %s
chown -R %s:%s %s
chmod -R 775 %s''' % ( ORACLE_BASE, USER_ORACLE, GROUP_OINSTALL, ORACLE_BASE, ORACLE_BASE )
    os.system( command )


def configure_kernel_parameters():
    '''Configures the kernel parameters for memory settings.'''
    
    print "Configuring kernel parameters ..."
    filename = "/etc/sysctl.conf"
    lines = \
'''
kernel.shmall = 2097152
kernel.shmmax = 536870912
kernel.shmmni = 4096
kernel.sem = 250 32000 100 128
fs.file-max = 658576
net.ipv4.ip_local_port_range = 1024 65000
net.core.rmem_default = 262144
net.core.wmem_default = 262144
net.core.rmem_max = 1048536
net.core.wmem_max = 1048536
'''
    f = open( filename, "a" )
    f.write( lines )
    f.close()
    os.system("sysctl -p > /dev/null") #activate
    
    
def configure_shell_limits():
    '''Configures shell security limits'''
    
    print "Configuring shell security limits ..."
    
    #---- Security Limits----- 
    filename = "/etc/security/limits.conf"
    lines = \
'''
%s soft nproc 2047
%s hard nproc 16384
%s soft nofile 1024
%s hard nofile 65536
''' % ( USER_ORACLE, USER_ORACLE, USER_ORACLE, USER_ORACLE )

    f = open( filename, "a" )
    f.write( lines )
    f.close()
    
    filename = "/etc/pam.d/login"
    f = open( filename, "a" )
    f.write( "session required /lib/security/pam_limits.so" )
    f.close()
    
    # --- /etc/profile -----
    filename = "/etc/profile"
    lines = \
'''
if [ \$USER = "%s" ]; then
 if [ \$SHELL = "/bin/ksh" ]; then
  ulimit -p 16384
  ulimit -n 65536
 else
  ulimit -u 16384 -n 65536
 fi
 umask 022
fi
''' % USER_ORACLE
    
    # Note: There was once a os.path.exists code here...???
    
    f = open( filename, "a" )
    f.write( lines )
    f.close()
    
    #----- csh.login----
    filename = "/etc/csh.login"
    lines=\
'''
if ( \$USER == "%s" ) then
limit maxproc 16384
limit descriptors 65536
umask 022
endif
EOF''' % USER_ORACLE
    
    f = open( filename, "a" )
    f.write( lines )
    f.close()
    
def configure_hangcheck_timer():
    '''Configures Hangcheck timer'''
    
    print "Configuring Hangcheck timer ..."
    command = "modprobe hangcheck-timer hangcheck_tick=30 hangcheck_margin=180"
    os.system( command )
    f = open( "/etc/rc.d/rc.local", "a" )
    f.write( command )
    f.close()


def configure_env_settings():
    '''Configures environment settings'''
        
    print "Configuring environment settings ..."    
    run_as( USER_ORACLE )
    filename = "/home/%s/.bash_profile" % USER_ORACLE
        
    lines = \
'''
# User specific environment and startup programs
umask 022
PATH=/bin:/usr/bin:/usr/local/bin:/usr/X11R6/bin
export LD_LIBRARY_PATH=/usr/lib:/usr/X11R6/lib
export ORACLE_BASE=%s
export ORACLE_HOME=$ORACLE_BASE%s
export ORACLE_SID=%s
PATH=$ORACLE_HOME/bin:$ORACLE_HOME/jdk/jre/lib/i386/server:$ORACLE_HOME/rdbms/lib:$ORACLE_HOME/lib:$LD_LIBRARY_PATH:/usr/kerberos/sbin:/usr/kerberos/bin:/usr/local/sbin:/sbin:/usr/sbin:/root/bin:$PATH
PATH=$PATH:$HOME/bin
export PATH
unset USERNAME
''' % ( ORACLE_BASE, ORACLE_HOME_POSTFIX, ORACLE_SID )
    
    f = open( filename, "a" )
    f.write( lines )
    f.close()
    os.system( "source ~/.bash_profile" )
    
    

# ---------------- PART 2 - INSTALLATION ---------------------------

def part2():
    print "#------------------------------------#"
    print "# Starting the Part 2 - Installation #"
    print "#                                    #"
    print "#------------------------------------#"
    unzip_the_setup_files()
    
def unzip_the_setup_files():
    '''Unzips the setup file'''
    
    run_as( "root" )
    print "Unzipping the setup file %s ..." % ZIP_FILE_PATH
    if not os.path.exists( ZIP_FILE_PATH ):
        print "The %s file does not exist. Exiting..." % ZIP_FILE_PATH
        return
       
    os.system( "xhost +" )
    run_as( USER_ORACLE )
    command = \
''' 
unzip %s -d %s
echo "Now starting the installer ..."
''' % ( ZIP_FILE_PATH, TEMP_SETUP_FILES )
    os.system( command )
    os.system('su - %s -c "sh %s/database/runInstaller"' % (USER_ORACLE, TEMP_SETUP_FILES))



def pre_configuration():
    part1()
    print "Waiting for 5 seconds before starting the installation... Press Ctrl+C to abort the installation"
    time.sleep( 5 )
    part2()
    
if __name__ == "__main__":
    pre_configuration()
