package com.snapgrid.viewmodel

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.snapgrid.data.remote.api.ApiService
import com.snapgrid.data.remote.dto.PostResponse
import dagger.hilt.android.lifecycle.HiltViewModel
import kotlinx.coroutines.flow.*
import kotlinx.coroutines.launch
import javax.inject.Inject

data class FeedState(
    val isLoading: Boolean = false,
    val posts: List<PostResponse> = emptyList(),
    val error: String? = null,
    val page: Int = 0
)

@HiltViewModel
class FeedViewModel @Inject constructor(
    private val apiService: ApiService
) : ViewModel() {

    private val _state = MutableStateFlow(FeedState())
    val state: StateFlow<FeedState> = _state.asStateFlow()

    fun loadFeed() {
        viewModelScope.launch {
            _state.update { it.copy(isLoading = true) }
            try {
                val response = apiService.getFeed()
                if (response.isSuccessful && response.body() != null) {
                    _state.update { it.copy(isLoading = false, posts = response.body()!!) }
                } else {
                    _state.update { it.copy(isLoading = false, error = response.message()) }
                }
            } catch (e: Exception) {
                _state.update { it.copy(isLoading = false, error = e.message) }
            }
        }
    }

    fun likePost(postId: Int) {
        viewModelScope.launch {
            try {
                val response = apiService.likePost(postId)
                if (response.isSuccessful && response.body() != null) {
                    val updatedPost = response.body()!!
                    _state.update { state ->
                        state.copy(
                            posts = state.posts.map { post ->
                                if (post.id == postId) post.copy(
                                    likesCount = updatedPost.likesCount,
                                    isLiked = updatedPost.isLiked
                                ) else post
                            }
                        )
                    }
                }
            } catch (e: Exception) {
                // Handle error silently for now
            }
        }
    }

    fun loadMore() {
        val nextPage = _state.value.page + 1
        viewModelScope.launch {
            try {
                val response = apiService.getFeed(skip = nextPage * 20)
                if (response.isSuccessful && response.body() != null) {
                    _state.update { state ->
                        state.copy(
                            posts = state.posts + response.body()!!,
                            page = nextPage
                        )
                    }
                }
            } catch (e: Exception) {
                // Handle error silently for now
            }
        }
    }
}