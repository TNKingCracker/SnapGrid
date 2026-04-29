package com.snapgrid.ui.navigation

import androidx.compose.foundation.layout.padding
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Add
import androidx.compose.material.icons.filled.Favorite
import androidx.compose.material.icons.filled.Home
import androidx.compose.material.icons.filled.Person
import androidx.compose.material.icons.filled.Search
import androidx.compose.material.icons.outlined.Home
import androidx.compose.material.icons.outlined.Search
import androidx.compose.material3.*
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.vector.ImageVector
import androidx.navigation.NavDestination.Companion.hierarchy
import androidx.navigation.NavGraph.Companion.findStartDestination
import androidx.navigation.NavHostController
import androidx.navigation.compose.NavHost
import androidx.navigation.compose.composable
import androidx.navigation.compose.currentBackStackEntryAsState
import androidx.navigation.compose.rememberNavController
import com.snapgrid.ui.screens.home.HomeScreen
import com.snapgrid.ui.screens.profile.ProfileScreen
import com.snapgrid.ui.screens.search.SearchScreen
import com.snapgrid.ui.screens.reels.ReelsScreen
import com.snapgrid.ui.screens.notifications.NotificationsScreen
import com.snapgrid.ui.screens.messages.MessagesScreen
import com.snapgrid.ui.screens.auth.LoginScreen

data class BottomNavItem(
    val route: String,
    val title: String,
    val selectedIcon: ImageVector,
    val unselectedIcon: ImageVector
)

val bottomNavItems = listOf(
    BottomNavItem("home", "Home", Icons.Filled.Home, Icons.Outlined.Home),
    BottomNavItem("search", "Search", Icons.Filled.Search, Icons.Outlined.Search),
    BottomNavItem("reels", "Reels", Icons.Filled.Home, Icons.Filled.Home),
    BottomNavItem("notifications", "Notifications", Icons.Filled.Favorite, Icons.Filled.Favorite),
    BottomNavItem("profile", "Profile", Icons.Filled.Person, Icons.Filled.Person)
)

@Composable
fun MainNavigation(
    isLoggedIn: Boolean
) {
    val navController = rememberNavController()
    
    if (isLoggedIn) {
        Scaffold(
            bottomBar = { BottomNavBar(navController) }
        ) { padding ->
            NavHost(
                navController = navController,
                startDestination = "home",
                modifier = Modifier.padding(padding)
            ) {
                composable("home") { HomeScreen(navController) }
                composable("search") { SearchScreen(navController) }
                composable("reels") { ReelsScreen(navController) }
                composable("notifications") { NotificationsScreen(navController) }
                composable("profile") { ProfileScreen(navController) }
            }
        }
    } else {
        NavHost(
            navController = navController,
            startDestination = "login"
        ) {
            composable("login") { LoginScreen(navController) }
        }
    }
}

@Composable
fun BottomNavBar(navController: NavHostController) {
    val navBackStackEntry by navController.currentBackStackEntryAsState()
    val currentDestination = navBackStackEntry?.destination
    
    NavigationBar {
        bottomNavItems.forEach { item ->
            val selected = currentDestination?.hierarchy?.any { it.route == item.route } == true
            NavigationBarItem(
                icon = {
                    Icon(
                        if (selected) item.selectedIcon else item.unselectedIcon,
                        contentDescription = item.title
                    )
                },
                label = { Text(item.title) },
                selected = selected,
                onClick = {
                    navController.navigate(item.route) {
                        popUpTo(navController.graph.findStartDestination().id) {
                            saveState = true
                        }
                        launchSingleTop = true
                        restoreState = true
                    }
                }
            )
        }
    }
}