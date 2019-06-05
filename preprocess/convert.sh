for i in download/Chinesee/*.wav;
   do name=`echo $i | cut -d'/' -f3`;
   ffmpeg -i "$i" "download/Chinese/${name}";
done
