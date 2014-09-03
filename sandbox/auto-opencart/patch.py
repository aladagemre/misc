#!/usr/bin/python
import os
OHOME = os.getenv('OHOME')
filename = "%s/install/view/template/step_3.tpl" % OHOME
print os.path.getsize(filename)
txt = open(filename).read()

txt = txt.replace("<?php echo $db_username; ?>", "<?php if ($db_username) echo $db_username; else echo getenv('DB_ENV_MYSQL_USER'); ?>")
txt = txt.replace("<?php echo $db_password; ?>", "<?php if ($db_password) echo $db_password; else echo getenv('DB_ENV_MYSQL_PASSWORD'); ?>")
txt = txt.replace("<?php echo $db_hostname; ?>", "<?php if ($db_hostname) echo $db_username; else echo getenv('DB_PORT_3306_TCP_ADDR'); ?>")
txt = txt.replace("<?php echo $db_databsae; ?>", "<?php if ($db_database) echo $db_database; else echo 'opencart'; ?>")

print "Writing..."
o = open(filename, "w")
o.write(txt)
o.close()

print "Wrote..."
print os.path.getsize(filename)
