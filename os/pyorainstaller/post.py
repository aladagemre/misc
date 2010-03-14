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

from config import *
from lib import *
import os


def main():
    part3()

if __name__ == "__main__":
    main()


# ---------------PART 3 - POST-CONFIGURATION ------------------------------
def part3():
    if os.getenv( "USER" ) != "root":
        run_as( ORACLE_USER )
    print "Starting Post-Installation Configurations..."
    create_dbora()
    link_dbora()
    fix_dbstart()
    flag_sid()
    set_ip()


post_configuration = part3



# ------------- Part 3 Functions --------------------
def create_dbora():
    '''Creates the /etc/init.d/dbora file'''
    print "Creating the /etc/init.d/dbora file ..."

    run_as( "root" )
    lines = \
'''
#!/bin/sh
# chkconfig: 345 99 10
# description: Oracle auto start-stop script.
#
# Set ORA_HOME to be equivalent to the $ORACLE_HOME
# from which you wish to execute dbstart and dbshut;
#
# Set ORA_OWNER to the user id of the owner of the 
# Oracle database in ORA_HOME.

ORA_HOME=%s
ORA_OWNER=%s

if [ ! -f $ORA_HOME/bin/dbstart ]
then
    echo "Oracle startup: cannot start"
    exit
fi

case "$1" in
    'start')
        # Start the Oracle databases:
        # The following command assumes that the oracle login 
        # will not prompt the user for any values
        su - $ORA_OWNER -c "$ORA_HOME/bin/lsnrctl start"
        su - $ORA_OWNER -c $ORA_HOME/bin/dbstart
	su - $ORA_OWNER -c "$ORA_HOME/bin/emctl start dbconsole"
        ;;
    'stop')
        # Stop the Oracle databases:
        # The following command assumes that the oracle login 
        # will not prompt the user for any values
	su - $ORA_OWNER -c "$ORA_HOME/bin/emctl stop dbconsole"
        su - $ORA_OWNER -c $ORA_HOME/bin/dbshut
        su - $ORA_OWNER -c "$ORA_HOME/bin/lsnrctl stop"

        ;;
esac

''' % ( ORACLE_HOME, USER_ORACLE )
    f = open( "/etc/init.d/dbora", "w" )
    f.write( lines )
    f.close()
    
    os.system( "chmod 755 /etc/init.d/dbora" )    
        
def link_dbora():
    '''Links the dbora script to rc.d levels'''

    print "Linking the dbora script to rc.d levels ..."
    command = \
'''
ln -s /etc/init.d/dbora /etc/rc3.d/S99dbora
ln -s /etc/init.d/dbora /etc/rc4.d/S99dbora
ln -s /etc/init.d/dbora /etc/rc5.d/S99dbora
ln -s /etc/init.d/dbora /etc/rc0.d/K10dbora
ln -s /etc/init.d/dbora /etc/rc6.d/K10dbora'''    
    os.system( command )
    
def fix_dbstart():
    '''Fixes the dbstart script's ORACLE_HOME_LISTNER parameter.'''
    print "Fixing the dbstart script's ORACLE_HOME_LISTNER parameter..."

    dbstart_file = open( DBSTART_FILE_PATH )
    output = ""
    for line in dbstart_file:
        if line.startswith( "ORACLE_HOME_LISTNER=" ):
            new_line = \
'''
# ------------------------------
#
# ORACLE_HOME_LISTNER=/ade/vikrkuma_new/oracle
# Note! The listener has been changed manually...
ORACLE_HOME_LISTNER=$ORACLE_HOME
#
#  ------------------------------
'''
            
            output += new_line
        else:
            output += line
    dbstart_file.close()
    dbstart_file = open( DBSTART_FILE_PATH, "w" )
    dbstart_file.write( output )
    dbstart_file.close()
    
def flag_sid():
    '''Opens the oratab file and sets the corresponding SID's flag to Y, meaning include the startup of this SID during the system startup'''

    print "Flagging the %s SID to be autostarted..."

    f = open( ORATAB_FILE_PATH )
    output = ""
    for line in f:
        if line.startswith( ORACLE_SID ):
            new_line = line[:-2] + 'Y\n'
        else:
            new_line = line
        
        output += new_line
    f.close()
    
    # Open again for writing this time
    f = open( ORATAB_FILE_PATH, "w" )
    f.write( output )

def set_ip():
    '''Sets the IP Address and Port of the server in tnsnamesora file.'''
    
    print "Configuring IP Address and port in tnsnamesora ..."
    f = open( TNSNAMESORA_FILE_PATH )
    output = ""
    for line in f:
        if line.startswith( "(ADDRESS = (PROTOCOL = TCP)(HOST = " ):
            new_line = "(ADDRESS = (PROTOCOL = TCP)(HOST = %s)(PORT = %s))" % ( IP_ADDRESS, PORT )
        else:
            new_line = line
        output += new_line
        
    f.close()
    
    # Open again for writing this time,
    f = open( TNSNAMESORA_FILE_PATH, "w" )
    f.write( output )
    f.close()
    
            
