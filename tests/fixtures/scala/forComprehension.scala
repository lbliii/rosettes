for {
  user <- findUser(id)
  profile <- fetchProfile(user.id)
  preferences <- loadPreferences(user.id)
} yield UserDetails(user, profile, preferences)