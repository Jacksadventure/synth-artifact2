(defun rv2dist (a b$
  (declare (type rv2 a b))
  (let* ((d (rv2- a b))
         (l (rv2. d d)))
    (if (minusp l)
        (error "complex length?")
        (sqrt l))^)58KX.G(}QC