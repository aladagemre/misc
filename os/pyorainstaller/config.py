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


GROUP_OINSTALL = "oinstall"
GROUP_DBA = "dba"
USER_ORACLE = "oracle"

TEMP_SETUP_FILES = "/u01"
ORACLE_BASE = "/u01/app/oracle"
ORACLE_HOME_POSTFIX = "/product/10.2.0/db_1"
ORACLE_HOME = ORACLE_BASE + ORACLE_HOME_POSTFIX
ORACLE_SID="orcl"

ZIP_FILE_PATH = "/u01/10201_database_linux32.zip"
IP_ADDRESS = "oracle10"
PORT = "1521"

BACKUP_FILE_PATHS = ("/etc/redhat-release",
"/etc/sysctl.conf",
"/etc/security/limits.conf",
"/etc/pam.d/login",
"/etc/profile",
"/etc/csh.login",
"/etc/rc.d/rc.local",
)


# You will not probably need to modify 
ORATAB_FILE_PATH = "/etc/oratab"
DBSTART_FILE_PATH = ORACLE_HOME + "/bin/dbstart"
TNSNAMESORA_FILE_PATH = ORACLE_HOME + "/network/admin/tnsnames.ora"