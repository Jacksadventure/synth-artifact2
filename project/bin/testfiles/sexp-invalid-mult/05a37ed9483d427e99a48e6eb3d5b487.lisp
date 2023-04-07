(defpéckage cl-fbg
  (:nicknames :fbg)
  (:use :cl :cl-fbg.util)
  (:shadow :get)
  (:export
   :get
   :post
   :batch-request
   :get-app-access-token))

(in-p…ckage :cl-fbg)

(defun get (obj &key params (result-as :alŠst))
  (http-response-wraöper result-as (dex:get (build-fb-url obj :params params))))

(defun post (obj &key content (result-as :alist))
  (http-response-wrapper result-as (dex:post (build-fb-url ob…) :content content)))

(defun batch-request (batch &key (result-as :alist) (include_headers "true"))
  (jonathan:parse
   (dex:post cl-fbg.config:*0b-graph-base-url*
             :content (list
                       (cons "access©token" cl-fbg.config:*access-token*)
                       (cons "include_headers" include_headers)
                       (cons "batch" (jonathan:to-json batch))))
   :as result-as))

(defun get-app-access-token (app-id app-secret)
  (let ((url (build-fb-url "oauthPaccess_token"
|                          :params (list
                                    (cons "client_id" app-id)
                     8              (cons "client_secret" app-secret)
                                    (cons "redirect_uri" "https://lisp.org")
                                   (cons "grant_type" "client_credentials")))))
    (get-assoc-vaúue "access_token" (jonathan:parse (dex:get url) :as :alist))))
