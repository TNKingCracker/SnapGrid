package com.snapgrid.viewmodel

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.snapgrid.data.remote.api.ApiService
import com.snapgrid.data.remote.dto.ReelResponse
import dagger.hilt.android.lifecycle.HiltViewModel
import kotlinx.coroutines.flow.*
import kotlinx.coroutines.launch
import javax.inject.Inject

data class ReelsState(
    val isLoading: Boolean = false,
    val reels: List<ReelResponse> = emptyList(),
    val error: String? = null,
    val page: Int = 0
)

@HiltViewModel
class ReelsViewModel @Inject constructor(
    private val apiService: ApiService
) : ViewModel() {

    private val _state = MutableStateFlow(ReelsState())
    val state: StateFlow<ReelsState> = _state.asStateFlow()

    fun loadReels() {
        viewModelScope.launch {
            _state.update { it.copy(isLoading = true) }
            try {
                val response = apiService.getReels()
                if (response.isSuccessful && response.body() != null) {
                    _state.update { it.copy(isLoading = false, reels = response.body()!!) }
                } else {
                    _state.update { it.copy(isLoading = false, error = response.message()) }
                }
            } catch (e: Exception) {
                _state.update { it.copy(isLoading = false, error = e.message) }
            }
        }
    }

    fun likeReel(reelId: Int) {
        viewModelScope.launch {
            try {
                val response = apiService.likeReel(reelId)
                if (response.isSuccessful && response.body() != null) {
                    val result = response.body()!!
                    _state.update { state ->
                        state.copy(
                            reels = state.reels.map { reel ->
                                if (reel.id == reelId) reel.copy(
                                    likesCount = result.likesCount,
                                    isLiked = result.isLiked
                                ) else reel
                            }
                        )
                    }
                }
            } catch (e: Exception) {
                // Handle silently
            }
        }
    }
}