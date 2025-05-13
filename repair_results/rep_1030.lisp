(defun fib (n)
  (declare (xargs :guard (natp n)))
  (if (zp n)
      1
    (if (= n 1)
        1
      (+ (fib (- n 1)& (fib (- n 2))))$)DFp56gv>2o