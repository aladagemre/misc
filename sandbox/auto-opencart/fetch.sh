git clone https://github.com/e-piksel/opencart-tr.git opencart
####cp -rf opencart/tam-surum/ana_dizine_yukleyin $OHOME # TR
export OROOT=${PWD}
export OHOME=${PWD}/opencart/tam-surum/ana_dizine_yukleyin

mkdir -p $OHOME/download $OHOME/image/data # TR
    
cd $OHOME && cp config-dist.php config.php && cp admin/config-dist.php admin/config.php && mkdir cache
cd $OHOME && chmod 0777 image/ image/cache/ cache/ download/ config.php admin/config.php image/data/ system/logs/ system/cache/
cd $OHOME && chmod 0777 system/download image/catalog  #TR

cd $OROOT
 
python patch.py


