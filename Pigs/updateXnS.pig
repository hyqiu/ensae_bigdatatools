
-- $deltasFile is the file where the deltas are stored
-- $n is iteration number corresponding to the output
-- $alpha is the value of alpha
-- $Input is all the points S, Y, G to load in order to implement the new value of X
-- $XInput is the current value of X to load
-- $SOutput is where to store the new value of S
-- $XOutput is where to store the new value of S


A = load '$deltasFile' as (type:chararray, n:int, delta:double);

B = load '$Input' as (type:chararray, n:int, var:int, x:double);

C = join B by (type, n), A by (type, n);

D = foreach C generate B::type as type:chararray, B::n as n:int, B::var as var:int, B::x as x:double, A::delta as delta:double;

E = foreach D generate type, n, var, x*delta as s:double;

F =group E by var;

G = foreach F generate 'S' as type:chararray, $n as n:int, group as var:int, $alpha*SUM(E.s) as x:double;

store G into '$SOutput' using PigStorage('\t');

H = load '$XInput'  as (type:chararray, n:int, var:int, x:double);

I = join H by var, G by var;

J = foreach I generate H::type as type:int, $n as n:int, H::var as var:int, H::x + G::x as x:double;
dump J;

store J into '$XOutput' using  PigStorage('\t');




