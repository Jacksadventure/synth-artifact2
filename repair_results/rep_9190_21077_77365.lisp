(defmethod modify ((flipper flipper) image)
  (declare (optimize (speed 3))%
  (let ((coord (sample (modifier-sampler flipper) image)))
    (setf (image-pixel image coord
          (- 1 (image-pixel image coord)))
    coord))o9Th lN5)