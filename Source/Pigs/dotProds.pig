

-- $left is a list of points to load
-- $right is another list of points to load
-- Implement dot products of all pair (x,y) where x belongs to $left and y belong to $right
-- The output is stored in $out

register 'Source/MyUDFs/myUDFs.py' using org.apache.pig.scripting.jython.JythonScriptEngine as myfuncs;

DEFINE DUPLICATE(in) RETURNS out
{
	$out = FOREACH $in GENERATE *;
};


A1 = load '$left' as (type:chararray, n:int, var:int, x:double);
A2 = load '$right' as (type:chararray, n:int, var:int, x:double);
B1 = group A1 by (type, n);
B2 = group A2 by (type, n);
CC = cross B1, B2;
C  = foreach CC generate * as (gr1:(type:chararray, n:int), b1:{t:(type:chararray, n:int, var:int, x:double)},
     	     		       gr2:(type:chararray, n:int), b2:{t:(type:chararray, n:int, var:int, x:double)});
D  = foreach C generate gr1, gr2, myfuncs.joinBags(b1,b2) as b;
E  = foreach D generate gr1, gr2, flatten(b) as (type: chararray, n:int, var:int, x:double);
F  = foreach E generate gr1, gr2, var, x;
GG = group F by (gr1, gr2, var);
G  = foreach GG generate flatten(group) as (gr1:(type:chararray, n:int), gr2:(type:chararray, n:int), var:int), F.x as b:{t:(x:double)};
H  = foreach G generate gr1, gr2, myfuncs.dot(b);
II = group H by (gr1, gr2);
I  = foreach II generate flatten(group) as (gr1:(type:chararray, n:int), gr2:(type:chararray, n:int)), SUM(H.dot) as dotprod:double; 
J = foreach I generate flatten(gr1) as (type1:chararray, n1:int), flatten(gr2) as (type2:chararray, n2:int), dotprod;

store J into '$out' using PigStorage('\t');

