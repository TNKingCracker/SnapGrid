package com.snapgrid.ui.screens.reels

import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Favorite
import androidx.compose.material.icons.filled.ChatBubble
import androidx.compose.material.icons.filled.Send
import androidx.compose.material.icons.filled.BookmarkBorder
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.layout.ContentScale
import androidx.compose.ui.unit.dp
import androidx.hilt.navigation.compose.hiltViewModel
import androidx.navigation.NavController
import coil.compose.AsyncImage
import com.snapgrid.data.remote.dto.ReelResponse
import com.snapgrid.viewmodel.ReelsViewModel

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun ReelsScreen(
    navController: NavController,
    viewModel: ReelsViewModel = hiltViewModel()
) {
    val state by viewModel.state.collectAsState()

    LaunchedEffect(Unit) {
        viewModel.loadReels()
    }

    Scaffold(
        topBar = {
            TopAppBar(title = { Text("Reels") })
        }
    ) { padding ->
        if (state.isLoading && state.reels.isEmpty()) {
            Box(
                modifier = Modifier.fillMaxSize().padding(padding),
                contentAlignment = Alignment.Center
            ) {
                CircularProgressIndicator()
            }
        } else if (state.reels.isEmpty()) {
            Box(
                modifier = Modifier.fillMaxSize().padding(padding),
                contentAlignment = Alignment.Center
            ) {
                Text("No reels yet")
            }
        } else {
            LazyColumn(
                modifier = Modifier.fillMaxSize().padding(padding)
            ) {
                items(state.reels) { reel ->
                    ReelItem(
                        reel = reel,
                        onLike = { viewModel.likeReel(reel.id) }
                    )
                }
            }
        }
    }
}

@Composable
fun ReelItem(
    reel: ReelResponse,
    onLike: () -> Unit
) {
    Card(
        modifier = Modifier
            .fillMaxWidth()
            .padding(8.dp)
    ) {
        Column {
            AsyncImage(
                model = reel.thumbnailUrl ?: reel.videoUrl,
                contentDescription = null,
                modifier = Modifier
                    .fillMaxWidth()
                    .aspectRatio(9f/16f),
                contentScale = ContentScale.Crop
            )
            Row(
                modifier = Modifier
                    .fillMaxWidth()
                    .padding(8.dp),
                verticalAlignment = Alignment.CenterVertically
            ) {
                IconButton(onClick = onLike) {
                    Icon(
                        Icons.Filled.Favorite,
                        contentDescription = "Like",
                        tint = if (reel.isLiked) MaterialTheme.colorScheme.error else LocalContentColor.current
                    )
                }
                Text("${reel.likesCount}")
                Spacer(modifier = Modifier.width(16.dp))
                IconButton(onClick = { }) {
                    Icon(Icons.Filled.ChatBubble, contentDescription = "Comment")
                }
                Text("${reel.commentsCount}")
                Spacer(modifier = Modifier.weight(1f))
                IconButton(onClick = { }) {
                    Icon(Icons.Filled.BookmarkBorder, contentDescription = "Save")
                }
            }
            if (!reel.caption.isNullOrBlank())) {
                Text(
                    text = reel.caption,
                    modifier = Modifier.padding(8.dp)
                )
            }
        }
    }
}