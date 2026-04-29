package com.snapgrid.viewmodel

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.snapgrid.data.remote.api.ApiService
import com.snapgrid.data.remote.dto.*
import com.snapgrid.data.repository.AuthRepository
import com.snapgrid.data.repository.Result
import com.snapgrid.utils.PreferencesManager
import dagger.hilt.android.lifecycle.HiltViewModel
import kotlinx.coroutines.flow.*
import kotlinx.coroutines.launch
import javax.inject.Inject

data class AuthState(
    val isLoading: Boolean = false,
    val isLoggedIn: Boolean = false,
    val user: UserResponse? = null,
    val error: String? = null
)

@HiltViewModel
class AuthViewModel @Inject constructor(
    private val authRepository: AuthRepository,
    private val preferencesManager: PreferencesManager
) : ViewModel() {

    private val _state = MutableStateFlow(AuthState())
    val state: StateFlow<AuthState> = _state.asStateFlow()

    init {
        viewModelScope.launch {
            _state.update { it.copy(isLoggedIn = authRepository.isLoggedIn()) }
        }
    }

    fun login(email: String, password: String) {
        viewModelScope.launch {
            _state.update { it.copy(isLoading = true, error = null) }
            when (val result = authRepository.login(email, password)) {
                is Result.Success -> {
                    val userResult = authRepository.getCurrentUser()
                    if (userResult is Result.Success) {
                        preferencesManager.saveUserInfo(userResult.data.id, userResult.data.username)
                    }
                    _state.update { it.copy(isLoading = false, isLoggedIn = true, user = userResult.data) }
                }
                is Result.Error -> {
                    _state.update { it.copy(isLoading = false, error = result.message) }
                }
            }
        }
    }

    fun register(email: String, username: String, password: String) {
        viewModelScope.launch {
            _state.update { it.copy(isLoading = true, error = null) }
            when (val result = authRepository.register(email, username, password)) {
                is Result.Success -> {
                    login(email, password)
                }
                is Result.Error -> {
                    _state.update { it.copy(isLoading = false, error = result.message) }
                }
            }
        }
    }

    fun logout() {
        viewModelScope.launch {
            authRepository.logout()
            _state.update { AuthState() }
        }
    }

    fun clearError() {
        _state.update { it.copy(error = null) }
    }
}