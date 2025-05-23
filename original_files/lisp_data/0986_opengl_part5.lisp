(defun main-loop ()
  (sdl:with-events ()
    (:quit-event () t)
    (:key-down-event (:key key)
                     (cond ((sdl:key= key :sdl-key-escape)
                            (sdl:push-quit-event))))
    (:idle ()
           (draw-update)
           (sdl:update-display))))