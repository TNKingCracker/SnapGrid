package com.snapgrid.viewmodel

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.snapgrid.data.remote.api.ApiService
import com.snapgrid.data.remote.dto.ConversationResponse
import dagger.hilt.android.lifecycle.HiltViewModel
import kotlinx.coroutines.flow.*
import kotlinx.coroutines.launch
import javax.inject.Inject

data class MessagesState(
    val isLoading: Boolean = false,
    val conversations: List<ConversationResponse> = emptyList(),
    val error: String? = null
)

@HiltViewModel
class MessageViewModel @Inject constructor(
    private val apiService: ApiService
) : ViewModel() {

    private val _state = MutableStateFlow(MessagesState())
    val state: StateFlow<MessagesState> = _state.asStateFlow()

    fun loadConversations() {
        viewModelScope.launch {
            _state.update { it.copy(isLoading = true) }
            try {
                val response = apiService.getConversations()
                if (response.isSuccessful && response.body() != null) {
                    _state.update { it.copy(isLoading = false, conversations = response.body()!!) }
                } else {
                    _state.update { it.copy(isLoading = false, error = response.message()) }
                }
            } catch (e: Exception) {
                _state.update { it.copy(isLoading = false, error = e.message) }
            }
        }
    }
}