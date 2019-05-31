for i in mp3/Chinese/*.wav;
   do name=`echo $i | cut -d'/' -f3`;
   ffmpeg -i "$i" "wav/Chinese/${name}";
done
