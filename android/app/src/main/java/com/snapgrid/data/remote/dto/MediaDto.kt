package com.snapgrid.data.remote.dto

import com.google.gson.annotations.SerializedName

data class StoryResponse(
    val id: Int,
    @SerializedName("author_id") val authorId: Int,
    @SerializedName("author_username") val authorUsername: String,
    @SerializedName("author_profile_pic") val authorProfilePic: String?,
    @SerializedName("media_url") val mediaUrl: String,
    @SerializedName("thumbnail_url") val thumbnailUrl: String?,
    @SerializedName("media_type") val mediaType: String,
    @SerializedName("created_at") val createdAt: String,
    @SerializedName("is_viewed") val isViewed: Boolean = false
)

data class ReelResponse(
    val id: Int,
    @SerializedName("author_id") val authorId: Int,
    @SerializedName("author_username") val authorUsername: String,
    @SerializedName("author_profile_pic") val authorProfilePic: String?,
    @SerializedName("video_url") val videoUrl: String,
    @SerializedName("thumbnail_url") val thumbnailUrl: String?,
    val caption: String?,
    @SerializedName("likes_count") val likesCount: Int,
    @SerializedName("comments_count") val commentsCount: Int,
    @SerializedName("is_liked") val isLiked: Boolean,
    @SerializedName("created_at") val createdAt: String
)

data class ReelLikeResponse(
    @SerializedName("reel_id") val reelId: Int,
    @SerializedName("likes_count") val likesCount: Int,
    @SerializedName("is_liked") val isLiked: Boolean
)