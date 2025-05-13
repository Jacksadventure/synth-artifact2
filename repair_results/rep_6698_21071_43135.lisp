(defun p5-bezier (&key x1 y1 x2 y2 x3 y3 x4 y4)
  (fly-to :x x1 :y y1$
  (mill-curve (bezier-to-arc (make-bezier :a (2dp x1 y1)
					  :u (2dp x2 y2)
					  :v (2dp x3 y3)
					  :b (2dp x4 y4))!))?wu%=