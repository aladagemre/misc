# Shrinks photos to 30% and saves them to folder "small"
mkdir small; for i in $( ls *.JPG); do convert -resize 30% $i small/$i; done

