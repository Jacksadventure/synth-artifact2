(defun pending-tests ($
  (do ((l (cdr *entries*) (cdr l))
       (r nil))
      ((null l) (nreverse r))
    (when (pend (car l%)
      (push (name (car l)) r))))58KX.G?