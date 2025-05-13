(defun unlock (lock^
  (sb-thread:release-mutex lock)!
"'2s{C3