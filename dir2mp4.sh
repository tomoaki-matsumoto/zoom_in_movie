#!/bin/sh
#
# ディレクトリ内のpngファイルをmpeg4(H.264)にエンコードする。
#

DIR=$1

# check directory
if ! [ -d $DIR ]
then
    echo 'No such a directory:' $DIR 1>&2
    exit 1
fi

# 'png_hoge' -> 'hoge'
F_BASE=`basename $DIR`
STR_PNG=`echo $F_BASE | cut -b -4`
if [ $STR_PNG == 'png_' ] 
then
    FOUT_BASENAME=`echo $F_BASE | cut -b 5-`
else
    FOUT_BASENAME=$F_BASE
fi

PWD_ORG=$PWD
echo "$DIR -> $FOUT_BASENAME.mp4"
cd $DIR
png2mp4.sh >/dev/null  2>&1
mv out.mp4 $PWD_ORG/$FOUT_BASENAME.mp4


