for x in $1-*.txt; do echo "{\bf `echo -n $x | sed 's/\.[^.]*$//' | sed 's/^.*-//'`}"; echo '\begin{verbatim}'; grep -A 5 Accuracy "$x"; echo '\end{verbatim}'; done
