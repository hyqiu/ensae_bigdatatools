
-- Implement the gradient of a function f at the point X given by $XInput
-- The gradient is stored in $GOutput
-- $GInput in the previous gradient
-- $GOuput - $GInput is stored in $YOutput


A = LOAD '$XInput' AS (type:chararray, n:int, var:int, x:double);

B = FOREACH A GENERATE 'G' as type:chararray, n as n:int, var as var:int, 2*x as g:double;

STORE B INTO '$GOutput' using PigStorage('\t');

C = load '$GInput' as (type:chararray, n:int, var:int, g:double);

D = join B by var, C by var;

E = foreach D generate 'Y' as type:chararray, B::n as n:int, B::var as var:int, B::g - C::g as y:double;

store E into '$YOutput' using PigStorage('\t');

