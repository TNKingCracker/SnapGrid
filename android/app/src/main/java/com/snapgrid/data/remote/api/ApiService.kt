package com.snapgrid.data.remote.api

import com.snapgrid.data.remote.dto.*
import okhttp3.MultipartBody
import okhttp3.RequestBody
import retrofit2.Response
import retrofit2.http.*

interface ApiService {

    @POST("auth/register")
    suspend fun register(@Body request: RegisterRequest): Response<UserResponse>

    @POST("auth/login")
    suspend fun login(@Body request: LoginRequest): Response<TokenResponse>

    @POST("auth/refresh")
    suspend fun refreshToken(@Body refreshToken: String): Response<TokenResponse>

    @GET("auth/me")
    suspend fun getCurrentUser(): Response<UserResponse>

    @GET("users/{userId}")
    suspend fun getUserById(@Path("userId") userId: Int): Response<UserDetailResponse>

    @GET("users/username/{username}")
    suspend fun getUserByUsername(@Path("username") username: String): Response<UserDetailResponse>

    @PUT("users/me")
    suspend fun updateProfile(@Body request: UserProfileUpdateRequest): Response<UserResponse>

    @Multipart
    @POST("users/me/profile-pic")
    suspend fun uploadProfilePicture(@Part file: MultipartBody.Part): Response<UserResponse>

    @GET("users/{userId}/followers")
    suspend fun getFollowers(
        @Path("userId") userId: Int,
        @Query("skip") skip: Int = 0,
        @Query("limit") limit: Int = 20
    ): Response<List<UserResponse>>

    @GET("users/{userId}/following")
    suspend fun getFollowing(
        @Path("userId") userId: Int,
        @Query("skip") skip: Int = 0,
        @Query("limit") limit: Int = 20
    ): Response<List<UserResponse>>

    @POST("users/{userId}/follow")
    suspend fun followUser(@Path("userId") userId: Int): Response<Map<String, String>>

    @DELETE("users/{userId}/follow")
    suspend fun unfollowUser(@Path("userId") userId: Int): Response<Map<String, String>>

    @Multipart
    @POST("posts")
    suspend fun createPost(
        @Part("caption") caption: RequestBody?,
        @Part("location") location: RequestBody?,
        @Part("media_type") mediaType: RequestBody,
        @Part media: MultipartBody.Part
    ): Response<PostResponse>

    @GET("posts/feed")
    suspend fun getFeed(
        @Query("skip") skip: Int = 0,
        @Query("limit") limit: Int = 20
    ): Response<List<PostResponse>>

    @GET("posts/user/{userId}")
    suspend fun getUserPosts(
        @Path("userId") userId: Int,
        @Query("skip") skip: Int = 0,
        @Query("limit") limit: Int = 20
    ): Response<List<PostResponse>>

    @GET("posts/{postId}")
    suspend fun getPost(@Path("postId") postId: Int): Response<PostResponse>

    @DELETE("posts/{postId}")
    suspend fun deletePost(@Path("postId") postId: Int): Response<Map<String, String>>

    @POST("posts/{postId}/like")
    suspend fun likePost(@Path("postId") postId: Int): Response<LikeResponse>

    @DELETE("posts/{postId}/like")
    suspend fun unlikePost(@Path("postId") postId: Int): Response<LikeResponse>

    @GET("posts/{postId}/comments")
    suspend fun getComments(
        @Path("postId") postId: Int,
        @Query("skip") skip: Int = 0,
        @Query("limit") limit: Int = 20
    ): Response<List<CommentResponse>>

    @POST("posts/{postId}/comments")
    suspend fun addComment(
        @Path("postId") postId: Int,
        @Body request: CommentCreateRequest
    ): Response<CommentResponse>

    @DELETE("posts/comments/{commentId}")
    suspend fun deleteComment(@Path("commentId") commentId: Int): Response<Map<String, String>>

    @GET("stories/following")
    suspend fun getStories(): Response<List<StoryResponse>>

    @Multipart
    @POST("stories")
    suspend fun createStory(
        @Part("media_type") mediaType: RequestBody,
        @Part file: MultipartBody.Part
    ): Response<StoryResponse>

    @POST("stories/{storyId}/view")
    suspend fun viewStory(@Path("storyId") storyId: Int): Response<Map<String, Any>>

    @GET("reels")
    suspend fun getReels(
        @Query("skip") skip: Int = 0,
        @Query("limit") limit: Int = 20
    ): Response<List<ReelResponse>>

    @Multipart
    @POST("reels")
    suspend fun createReel(
        @Part("caption") caption: RequestBody?,
        @Part file: MultipartBody.Part
    ): Response<ReelResponse>

    @POST("reels/{reelId}/like")
    suspend fun likeReel(@Path("reelId") reelId: Int): Response<ReelLikeResponse>

    @GET("messages/conversations")
    suspend fun getConversations(): Response<List<ConversationResponse>>

    @GET("messages/{userId}")
    suspend fun getMessages(
        @Path("userId") userId: Int,
        @Query("skip") skip: Int = 0,
        @Query("limit") limit: Int = 50
    ): Response<List<MessageResponse>>

    @POST("messages/{userId}")
    suspend fun sendMessage(
        @Path("userId") userId: Int,
        @Body request: MessageCreateRequest
    ): Response<MessageResponse>

    @GET("notifications")
    suspend fun getNotifications(
        @Query("skip") skip: Int = 0,
        @Query("limit") limit: Int = 20
    ): Response<List<NotificationResponse>>

    @PUT("notifications/{notificationId}/read")
    suspend fun markNotificationRead(@Path("notificationId") notificationId: Int): Response<Map<String, String>>

    @PUT("notifications/read-all")
    suspend fun markAllNotificationsRead(): Response<Map<String, String>>

    @GET("search")
    suspend fun searchUsers(@Query("q") query: String): Response<List<UserResponse>>

    @GET("search/posts")
    suspend fun searchPosts(@Query("q") query: String): Response<List<PostResponse>>

    @GET("search/explore")
    suspend fun explorePosts(
        @Query("skip") skip: Int = 0,
        @Query("limit") limit: Int = 20
    ): Response<List<PostResponse>>
}