
data work.ordered_try;
    set work.ordered;
    line_num = _N_;
    retain sum_score;
    if _N_ = 1 then sum_score = 0;
    avg_score = sum_score / _N_;
    sum_score = sum_score + score;
    if score >= avg_score
        then diff_score = score - avg_score;
    else diff_score = avg_score - score;
run;

ods noproctitle;
ods graphics / imagemap=on;

proc univariate data=WORK.ORDERED_TRY;
	ods select Histogram;
	var diff_score avg_score score;
	histogram diff_score avg_score score;
run;
proc corr data=WORK.ORDERED_TRY pearson hoeffding nosimple 
		plots(maxpoints=none)=matrix(histogram);
	var score diff_score avg_score;
	with score diff_score avg_score;
run;



