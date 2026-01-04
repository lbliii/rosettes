package com.example

import scala.concurrent.{Future, ExecutionContext}
import scala.util.{Try, Success, Failure}

case class User(id: Long, name: String, email: Option[String])

object UserService {
  def findById(id: Long)(implicit ec: ExecutionContext): Future[Option[User]] = Future {
    Some(User(id, "Alice", Some("alice@example.com")))
  }
}