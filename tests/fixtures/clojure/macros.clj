(defmacro when [test & body]
  `(if ~test (do ~@body)))

(when true
  (println "It's true!"))