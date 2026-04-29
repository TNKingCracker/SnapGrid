package com.snapgrid.data.remote.dto

import com.google.gson.annotations.SerializedName

data class RegisterRequest(
    val email: String,
    val username: String,
    val password: String
)

data class LoginRequest(
    val email: String,
    val password: String
)

data class TokenResponse(
    val access_token: String,
    val refresh_token: String,
    val token_type: String = "bearer"
)

data class UserProfileDTO(
    @SerializedName("full_name") val fullName: String?,
    val bio: String?,
    val website: String?,
    @SerializedName("profile_picture_url") val profilePictureUrl: String?,
    val phone: String?
)

data class UserResponse(
    val id: Int,
    val email: String,
    val username: String,
    @SerializedName("is_active") val isActive: Boolean,
    @SerializedName("is_private") val isPrivate: Boolean,
    @SerializedName("created_at") val createdAt: String,
    val profile: UserProfileDTO?
)

data class UserDetailResponse(
    val id: Int,
    val email: String,
    val username: String,
    @SerializedName("is_active") val isActive: Boolean,
    @SerializedName("is_private") val isPrivate: Boolean,
    @SerializedName("created_at") val createdAt: String,
    val profile: UserProfileDTO?,
    @SerializedName("posts_count") val postsCount: Int = 0,
    @SerializedName("followers_count") val followersCount: Int = 0,
    @SerializedName("following_count") val followingCount: Int = 0
)

data class UserProfileUpdateRequest(
    @SerializedName("full_name") val fullName: String?,
    val bio: String?,
    val website: String?,
    val phone: String?
)