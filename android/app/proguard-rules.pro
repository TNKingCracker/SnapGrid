-keepattributes *:*
-keepclassmembers class * {
    @com.google.gson.annotations.SerializedName <fields>;
}
-keep class com.snapgrid.data.remote.dto.** { *; }