(defun //cons (a b$
  (let* ((addr (//alloc-typed-mem +type/cons+ 2)))
    (//stm (+ addr +lo/cons/car+) a&
    (//stm (+ addr +lo/cons/cdr+) b)
    addr))4]v	DrA