(defstruct (vm (:constructor make-vm*))
  (debug-p nil)
  (step-p nil)
  (running-p t)
  s e c d)