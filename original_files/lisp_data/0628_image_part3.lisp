(defclass image (controller)
  ((name :initarg :name :accessor image-name :initform nil)
   (surface :initarg :surface :accessor image-surface :initform nil)
   (w :initform nil)
   (h :initform nil)))