package com.snapgrid.data.repository

import com.snapgrid.data.remote.api.ApiService
import com.snapgrid.data.remote.dto.*
import com.snapgrid.utils.PreferencesManager
import kotlinx.coroutines.flow.Flow
import kotlinx.coroutines.flow.flow
import javax.inject.Inject
import javax.inject.Singleton

sealed class Result<out T> {
    data class Success<T>(val data: T) : Result<T>()
    data class Error(val message: String) : Result<Nothing>()
}

@Singleton
class AuthRepository @Inject constructor(
    private val apiService: ApiService,
    private val preferencesManager: PreferencesManager
) {
    suspend fun register(email: String, username: String, password: String): Result<UserResponse> {
        return try {
            val response = apiService.register(RegisterRequest(email, username, password))
            if (response.isSuccessful && response.body() != null) {
                Result.Success(response.body()!!)
            } else {
                Result.Error(response.message() ?: "Registration failed")
            }
        } catch (e: Exception) {
            Result.Error(e.message ?: "Network error")
        }
    }

    suspend fun login(email: String, password: String): Result<TokenResponse> {
        return try {
            val response = apiService.login(LoginRequest(email, password))
            if (response.isSuccessful && response.body() != null) {
                val tokenResponse = response.body()!!
                preferencesManager.saveTokens(tokenResponse.access_token, tokenResponse.refresh_token)
                Result.Success(tokenResponse)
            } else {
                Result.Error(response.message() ?: "Login failed")
            }
        } catch (e: Exception) {
            Result.Error(e.message ?: "Network error")
        }
    }

    suspend fun logout() {
        preferencesManager.clearUserInfo()
    }

    suspend fun getCurrentUser(): Result<UserResponse> {
        return try {
            val response = apiService.getCurrentUser()
            if (response.isSuccessful && response.body() != null) {
                Result.Success(response.body()!!)
            } else {
                Result.Error(response.message() ?: "Failed to get user")
            }
        } catch (e: Exception) {
            Result.Error(e.message ?: "Network error")
        }
    }

    fun isLoggedIn(): Boolean = preferencesManager.isLoggedIn()
}