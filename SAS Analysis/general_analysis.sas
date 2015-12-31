/* general discription */
ods noproctitle;
/* analyze numeric variables */
title "Descriptive Statistics for Numeric Variables";
proc means data=WORK.IMPORT n nmiss min mean median max std;
	var score support against replyno year month day hour minute second;
run;
proc univariate data=WORK.IMPORT noprint;
	histogram score support against replyno year month day hour minute second;
run;
title;
/* bar chart */
title1 "Bar Chart";
ods graphics / reset imagemap;
/* records - year */
title2 "Records Per Year";
proc sgplot data=WORK.ORDERED;
	vbar year / name='Year';
	yaxis label="Counts" grid;
run;
/* records - month */
title2 "Records Per Month";
proc sgplot data=WORK.ORDERED;
	vbar year / group=month groupdisplay=Cluster name='Month & Year';
	yaxis grid;
run;
/* records - day */
title2 "Records Per Day";
proc sgplot data=WORK.ORDERED;
	vbar month / group=day groupdisplay=Stack datalabel name='Day & Month';
	yaxis grid;
run;
/* records - response */
title2 "Records Per Replynumber";
proc sgplot data=WORK.ORDERED;
	vbar replyno / name='Replies';
	yaxis grid;
run;
title2 "Records Per Supportnumber";
proc sgplot data=WORK.ORDERED;
	vbar support / name='Supports';
	yaxis grid;
run;
title2 "Records Per Againstnumber";
proc sgplot data=WORK.ORDERED;
	vbar against / name='Againsts';
	yaxis grid;
run;
/* Sequence Charts */
title1 "Series Chart";
title2 "Score - Time";
proc sgplot data=WORK.ORDERED;
	series x=datemark y=score / group=year transparency=0.0 name='Series';
	xaxis grid;
	yaxis grid;
run;
title2 "Replies - Time";
proc sgplot data=WORK.ORDERED;
	series x=datemark y=replyno / group=year transparency=0.0 name='Series';
	xaxis grid;
	yaxis grid;
run;
title2 "Supports - Time";
proc sgplot data=WORK.ORDERED;
	series x=datemark y=support / group=year transparency=0.0 name='Series';
	xaxis grid;
	yaxis grid;
run;
title2 "Againsts - Time";
proc sgplot data=WORK.ORDERED;
	series x=datemark y=against / group=year transparency=0.0 name='Series';
	xaxis grid;
	yaxis grid;
run;
ods graphics / reset;
title;