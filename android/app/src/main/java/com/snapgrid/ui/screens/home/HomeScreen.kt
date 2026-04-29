package com.snapgrid.ui.screens.home

import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Add
import androidx.compose.material.icons.filled.Favorite
import androidx.compose.material.icons.filled.ChatBubble
import androidx.compose.material.icons.filled.Send
import androidx.compose.material.icons.filled.MoreVert
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.layout.ContentScale
import androidx.compose.ui.unit.dp
import androidx.hilt.navigation.compose.hiltViewModel
import androidx.navigation.NavController
import coil.compose.AsyncImage
import com.snapgrid.data.remote.api.ApiService
import com.snapgrid.data.remote.dto.PostResponse
import com.snapgrid.ui.components.PostCard
import com.snapgrid.ui.navigation.Screen
import com.snapgrid.viewmodel.FeedViewModel

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun HomeScreen(
    navController: NavController,
    viewModel: FeedViewModel = hiltViewModel()
) {
    val state by viewModel.state.collectAsState()

    LaunchedEffect(Unit) {
        viewModel.loadFeed()
    }

    Scaffold(
        topBar = {
            TopAppBar(
                title = { Text("SnapGrid") },
                actions = {
                    IconButton(onClick = { navController.navigate(Screen.CreatePost.route) }) {
                        Icon(Icons.Filled.Add, contentDescription = "Create Post")
                    }
                    IconButton(onClick = { navController.navigate(Screen.Messages.route) }) {
                        Icon(Icons.Filled.ChatBubble, contentDescription = "Messages")
                    }
                }
            )
        }
    ) { padding ->
        if (state.isLoading && state.posts.isEmpty()) {
            Box(
                modifier = Modifier
                    .fillMaxSize()
                    .padding(padding),
                contentAlignment = Alignment.Center
            ) {
                CircularProgressIndicator()
            }
        } else if (state.posts.isEmpty()) {
            Box(
                modifier = Modifier
                    .fillMaxSize()
                    .padding(padding),
                contentAlignment = Alignment.Center
            ) {
                Text(
                    text = "No posts yet. Follow some users!",
                    style = MaterialTheme.typography.bodyLarge
                )
            }
        } else {
            LazyColumn(
                modifier = Modifier
                    .fillMaxSize()
                    .padding(padding)
            ) {
                items(state.posts) { post ->
                    PostCard(
                        post = post,
                        onLike = { viewModel.likePost(post.id) },
                        onComment = { /* Navigate to comments */ },
                        onShare = { /* Share post */ }
                    )
                }
            }
        }
    }
}