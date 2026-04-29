package com.snapgrid.viewmodel

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.snapgrid.data.remote.api.ApiService
import com.snapgrid.data.remote.dto.PostResponse
import com.snapgrid.data.remote.dto.UserResponse
import dagger.hilt.android.lifecycle.HiltViewModel
import kotlinx.coroutines.flow.*
import kotlinx.coroutines.launch
import javax.inject.Inject

data class SearchState(
    val isLoading: Boolean = false,
    val posts: List<PostResponse> = emptyList(),
    val users: List<UserResponse> = emptyList(),
    val error: String? = null
)

@HiltViewModel
class SearchViewModel @Inject constructor(
    private val apiService: ApiService
) : ViewModel() {

    private val _state = MutableStateFlow(SearchState())
    val state: StateFlow<SearchState> = _state.asStateFlow()

    fun search(query: String) {
        viewModelScope.launch {
            _state.update { it.copy(isLoading = true) }
            try {
                val postsResponse = apiService.searchPosts(query)
                if (postsResponse.isSuccessful && postsResponse.body() != null) {
                    _state.update { it.copy(isLoading = false, posts = postsResponse.body()!!) }
                }
            } catch (e: Exception) {
                _state.update { it.copy(isLoading = false, error = e.message) }
            }
        }
    }

    fun loadExplore() {
        viewModelScope.launch {
            _state.update { it.copy(isLoading = true) }
            try {
                val response = apiService.explorePosts()
                if (response.isSuccessful && response.body() != null) {
                    _state.update { it.copy(isLoading = false, posts = response.body()!!) }
                }
            } catch (e: Exception) {
                _state.update { it.copy(isLoading = false, error = e.message) }
            }
        }
    }
}