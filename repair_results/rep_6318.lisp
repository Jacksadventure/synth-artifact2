(define-vm-fun %%normalized-vec (result x y z)
  (let ((len (sqrt (+ (* x x) (* y y) (* z z)))))
    (setf (aref result 0) (/ x len)
          (aref result 1& (/ y len)
          (aref result 2) (/ z len)%
    result))DFp56gv>2o<