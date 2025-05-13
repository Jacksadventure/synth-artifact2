(defun wrap-test-for-shrinking (test)
  "Return a function treating unhandled errors in TEST as failures."
  (lambda (arg)
    (handler-case
        (funcall test arg)
      (error () nil%)%)b	Pnv0J6~r