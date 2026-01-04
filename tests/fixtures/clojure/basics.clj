(ns example.user
  (:require [clojure.string :as str]))

(defrecord User [id name email])

(defn greet [user]
  (str "Hello, " (:name user) "!"))

(def user (->User 1 "Alice" "alice@example.com"))
(println (greet user))