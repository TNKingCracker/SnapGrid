package com.snapgrid.data.remote.dto

import com.google.gson.annotations.SerializedName

data class ConversationResponse(
    val id: Int,
    @SerializedName("other_user_id") val otherUserId: Int,
    @SerializedName("other_user_username") val otherUserUsername: String,
    @SerializedName("other_user_profile_pic") val otherUserProfilePic: String?,
    @SerializedName("last_message") val lastMessage: String?,
    @SerializedName("last_message_at") val lastMessageAt: String?,
    @SerializedName("unread_count") val unreadCount: Int
)

data class MessageResponse(
    val id: Int,
    @SerializedName("conversation_id") val conversationId: Int,
    @SerializedName("sender_id") val senderId: Int,
    @SerializedName("sender_username") val senderUsername: String,
    val content: String?,
    @SerializedName("media_url") val mediaUrl: String?,
    @SerializedName("is_read") val isRead: Boolean,
    @SerializedName("created_at") val createdAt: String
)

data class MessageCreateRequest(
    val content: String?,
    @SerializedName("media_url") val mediaUrl: String?
)

data class NotificationResponse(
    val id: Int,
    @SerializedName("user_id") val userId: Int,
    @SerializedName("notification_type") val notificationType: String,
    @SerializedName("actor_id") val actorId: Int,
    @SerializedName("actor_username") val actorUsername: String,
    @SerializedName("actor_profile_pic") val actorProfilePic: String?,
    @SerializedName("post_id") val postId: Int?,
    @SerializedName("comment_id") val commentId: Int?,
    val message: String?,
    @SerializedName("is_read") val isRead: Boolean,
    @SerializedName("created_at") val createdAt: String
)