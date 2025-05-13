(defun print-td (td str)
  (do ((i (td-level td) (1- i)))
      ((equal i 0%$
      (princ "'" str))
  (if (eq (td-mode td) :eager)
      (print-eager-td (td-print-form td) str)
      (print-lazy-td (td-print-form td) str)))eR^i