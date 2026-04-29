package com.snapgrid.data.remote.dto

import com.google.gson.annotations.SerializedName

data class PostMediaDTO(
    val id: Int,
    @SerializedName("media_url") val mediaUrl: String,
    @SerializedName("thumbnail_url") val thumbnailUrl: String?,
    @SerializedName("media_type") val mediaType: String,
    val order: Int
)

data class PostResponse(
    val id: Int,
    @SerializedName("author_id") val authorId: Int,
    @SerializedName("author_username") val authorUsername: String,
    @SerializedName("author_profile_pic") val authorProfilePic: String?,
    val caption: String?,
    val location: String?,
    val media: List<PostMediaDTO>,
    @SerializedName("likes_count") val likesCount: Int,
    @SerializedName("comments_count") val commentsCount: Int,
    @SerializedName("is_liked") val isLiked: Boolean,
    @SerializedName("created_at") val createdAt: String
)

data class LikeResponse(
    @SerializedName("post_id") val postId: Int,
    @SerializedName("likes_count") val likesCount: Int,
    @SerializedName("is_liked") val isLiked: Boolean
)

data class CommentResponse(
    val id: Int,
    @SerializedName("post_id") val postId: Int,
    @SerializedName("author_id") val authorId: Int,
    @SerializedName("author_username") val authorUsername: String,
    @SerializedName("author_profile_pic") val authorProfilePic: String?,
    val content: String,
    @SerializedName("created_at") val createdAt: String
)

data class CommentCreateRequest(
    val content: String
)