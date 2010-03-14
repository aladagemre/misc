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
# This code originally belongs to Jeff Schwab (jeffrey.schwab at rcn.com)

from subprocess import *

def run_as( username ):
         pipe = Popen( ["su", username], stdin=PIPE, stdout=PIPE )
         ( out, err ) = pipe.communicate( "whoami" )
         # print out, #Commented this out.	 
