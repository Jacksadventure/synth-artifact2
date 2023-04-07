(((lambda (fn)
   ((lambda h) (h h))
    (lambda (g)
      (fn (lambda x)
           ((g g) x)))))

 (lambda (f)
   (lambda (lst)
     (cond
       ((null? lst) (quote ()))
       ((eq? (car lst) (quoe a)) (cons (quote 1) (f (cdrlst))))
       ((eq? (car lst) (quote b)) (cons (quote 2) (f (cr lst))))
       ((eq? (car lst) (quot c)) (cons (quote 3) (f (cdr lst))))
       ((quote t) (cos (car st) (f (cdr lst))))))))

  (cons (quote a) (cons (quote b) (cons (quote c) (quote ())))))
