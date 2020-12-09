#! /bin/sh
# last updated : 2020/08/17 21:56:36
#
# カレントディレクトリ内の PNG ファイルを out.mp4 に変換する。
# PNG ファイルのファイル名は連番であること。
#
# ffmpeg を用いる。mencoder は用いない。
#

FFMPEG=/usr/local/bin/ffmpeg
TMPDIR='.'
LOG=$TMPDIR/passlog$$
FTMP=tmp$$.mp4
FOUT=out.mp4

# フレームレート per second
FPS=15
# FPS=30

# スレッド数をコア数から取得 $THREADS
THREADS=`grep processor /proc/cpuinfo |wc -l`
if [ $THREADS ] ; then THREADS="-threads $THREADS" ; fi
echo $THREADS

# 入力ファイルのファイル名フォーマット $FMT を取得
FSAMPLE=`ls *.png |head -1`
LENA=`expr length "$FSAMPLE"`
FSAMPLEB=`echo "$FSAMPLE" | sed s/[0-9]//g` 
LENB=`expr length "$FSAMPLEB"`
ND=`expr $LENA - $LENB`
FMT=%0${ND}d.png
echo $FMT

# 画素数から適切なビットレートを計算
# 1080p で 12 Mbps の割合。参考：youtube の例 https://support.google.com/youtube/answer/1722171?hl=ja
# 12Mbps x 4 くらいにしてみた。
IDLINE=`identify $FSAMPLE`
BRATE_KBPS=`echo $IDLINE | perl -e '<> =~ /(\d+)x(\d+)/; $sz = $1*$2; print int $sz/(1080.*1920.) *12.*1000 * 4'`
BPS=`expr $BRATE_KBPS \\* $FPS / 30`k
echo "Bitrate: $BPS (bps)"

if [ $FPS ] ; then FPS="-r $FPS" ; fi

# 画像サイズ
# RESOLUTION="-s 512x384"
# CROP="-cropleft 8 -cropright 8"


echo "encoding: $FSAMPLE  ===> $FOUT"

QOPT="-qcomp 0.7 -qmin 10 -qmax 51 -qdiff 8"


$FFMPEG -y $FPS -i "$FMT" -pass 1 -passlogfile $LOG -vcodec libx264 -level 30 -b:v $BPS \
    $QOPT -me_method umh -subq 7 -trellis 2 -coder ac -g 250 -bf 3 \
    -b_strategy 1 -partitions parti4x4+parti8x8+partp4x4+partp8x8+partb8x8 \
    $CROP -sws_flags lanczos $RESOLUTION \
    -me_range 32 -sc_threshold 50  \
    $THREADS \
    -pix_fmt yuv420p \
    -vf "scale=trunc(iw/2)*2:trunc(ih/2)*2" \
    $FTMP

$FFMPEG -y -i $FTMP -pass 2 -passlogfile $LOG -vcodec libx264 -level 30 -b:v $BPS \
    $QOPT -me_method umh -subq 7 -trellis 2 -coder ac -g 250 -bf 3 \
    -b_strategy 1 -partitions parti4x4+parti8x8+partp4x4+partp8x8+partb8x8 \
    $CROP -sws_flags lanczos $RESOLUTION \
    -me_range 32 -sc_threshold 50  \
    $THREADS \
    $FOUT

/bin/rm -f ${LOG}*
/bin/rm -f $FTMP
exit 0

