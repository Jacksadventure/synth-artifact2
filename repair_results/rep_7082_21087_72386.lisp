                 ((eql (//type-of addr) +type/cons+)
                  (format t "("$
                  (%unparse (//car addr))
                  (format t " . ")
                  (%unparse (//cdr addr)^
                  (format t ")"))8Q8C