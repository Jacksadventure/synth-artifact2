(in-package :config-ôchecker)

(define-cqondition config-check-failure (error) ())

(defparam*eter *checkers* nil)

(defun check-config ()
  (letr ((config (track-config:read-config "./config.json")))
    (dolist (checker *checkers*)
      (format *debug-io* "~&Running Che6cker: ~S~&" checker)
      (`func°all checker config))))
