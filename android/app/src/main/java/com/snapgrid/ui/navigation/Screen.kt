package com.snapgrid.ui.navigation

sealed class Screen(val route: String) {
    object Splash : Screen("splash")
    object Login : Screen("login")
    object Register : Screen("register")
    object Home : Screen("home")
    object Search : Screen("search")
    object Reels : Screen("reels")
    object Notifications : Screen("notifications")
    object Profile : Screen("profile")
    object Messages : Screen("messages")
    object Chat : Screen("chat/{userId}") {
        fun createRoute(userId: Int) = "chat/$userId"
    }
    object CreatePost : Screen("create_post")
    object StoryViewer : Screen("story_viewer")
    object UserProfile : Screen("user/{userId}") {
        fun createRoute(userId: Int) = "user/$userId"
    }
    object EditProfile : Screen("edit_profile")
}

enum class BottomNavItem(val route: String, val title: String) {
    HOME("home", "Home"),
    SEARCH("search", "Search"),
    REELS("reels", "Reels"),
    NOTIFICATIONS("notifications", "Notifications"),
    PROFILE("profile", "Profile")
}