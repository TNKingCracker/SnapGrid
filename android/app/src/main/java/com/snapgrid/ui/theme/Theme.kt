package com.snapgrid.ui.theme

import androidx.compose.foundation.isSystemInDarkTheme
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.darkColorScheme
import androidx.compose.material3.lightColorScheme
import androidx.compose.runtime.Composable
import androidx.compose.ui.graphics.Color

private val DarkColorScheme = darkColorScheme(
    primary = Pink500,
    onPrimary = White,
    secondary = Blue500,
    onSecondary = White,
    background = Black,
    onBackground = White,
    surface = Gray900,
    onSurface = White,
    surfaceVariant = Gray800,
    onSurfaceVariant = Gray300,
)

private val LightColorScheme = lightColorScheme(
    primary = Pink500,
    onPrimary = White,
    secondary = Blue500,
    onSecondary = White,
    background = White,
    onBackground = Black,
    surface = Gray50,
    onSurface = Black,
    surfaceVariant = Gray100,
    onSurfaceVariant = Gray600,
)

@Composable
fun SnapGridTheme(
    darkTheme: Boolean = isSystemInDarkTheme(),
    content: @Composable () -> Unit
) {
    val colorScheme = if (darkTheme) DarkColorScheme else LightColorScheme
    MaterialTheme(
        colorScheme = colorScheme,
        content = content
    )
}