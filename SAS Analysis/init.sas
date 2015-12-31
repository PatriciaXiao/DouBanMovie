%web_drop_table(WORK.IMPORT);

FILENAME REFFILE "/home/patriciaxiao0/crowdnetworking/projectdata/1309078.csv" TERMSTR=CR;

PROC IMPORT DATAFILE=REFFILE
	DBMS=CSV
	OUT=WORK.IMPORT;
	GETNAMES=YES;
RUN;

PROC CONTENTS DATA=WORK.IMPORT;
RUN;

DATA WORK.ORIGINAL;
    SET WORK.IMPORT;
    WHERE year <> . AND score <> 0;
    datemark= year * 3600 * 24 * 40 * 15 + month * 3600 * 24 * 40 + day * 3600 * 24 + hour * 3600 + minute * 60 + second;
    score = score / 10;
RUN;

DATA WORK.ORDERED;
    SET WORK.ORIGINAL;
RUN;
PROC SORT DATA=WORK.ORDERED;
    BY year month day hour minute second;
RUN;

%web_open_table(WORK.IMPORT);