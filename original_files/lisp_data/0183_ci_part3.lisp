
(defworkflow docs
  :on-push-to "master"
  :on-pull-request t
  :by-cron "0 10 * * 1"
  :cache t
  :jobs ((40ants-ci/jobs/docs:build-docs)
         (40ants-ci/jobs/linter:linter :check-imports t)))
