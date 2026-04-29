package com.snapgrid.viewmodel

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.snapgrid.data.remote.api.ApiService
import com.snapgrid.data.remote.dto.PostResponse
import com.snapgrid.data.remote.dto.UserDetailResponse
import com.snapgrid.data.repository.AuthRepository
import dagger.hilt.android.lifecycle.HiltViewModel
import kotlinx.coroutines.flow.*
import kotlinx.coroutines.launch
import javax.inject.Inject

data class ProfileState(
    val isLoading: Boolean = false,
    val user: UserDetailResponse? = null,
    val posts: List<PostResponse> = emptyList(),
    val error: String? = null
)

@HiltViewModel
class ProfileViewModel @Inject constructor(
    private val apiService: ApiService,
    private val authRepository: AuthRepository
) : ViewModel() {

    private val _state = MutableStateFlow(ProfileState())
    val state: StateFlow<ProfileState> = _state.asStateFlow()

    fun loadProfile() {
        viewModelScope.launch {
            _state.update { it.copy(isLoading = true) }
            try {
                val userResponse = apiService.getCurrentUser()
                if (userResponse.isSuccessful && userResponse.body() != null) {
                    val user = userResponse.body()!!
                    _state.update { it.copy(user = user) }
                    
                    val postsResponse = apiService.getUserPosts(user.id)
                    if (postsResponse.isSuccessful && postsResponse.body() != null) {
                        _state.update { it.copy(isLoading = false, posts = postsResponse.body()!!) }
                    } else {
                        _state.update { it.copy(isLoading = false) }
                    }
                } else {
                    _state.update { it.copy(isLoading = false, error = userResponse.message()) }
                }
            } catch (e: Exception) {
                _state.update { it.copy(isLoading = false, error = e.message) }
            }
        }
    }

    fun logout() {
        viewModelScope.launch {
            authRepository.logout()
        }
    }
}