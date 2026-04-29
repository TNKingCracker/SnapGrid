package com.snapgrid

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.compose.runtime.collectAsState
import androidx.compose.runtime.getValue
import androidx.hilt.navigation.compose.hiltViewModel
import com.snapgrid.ui.navigation.MainNavigation
import com.snapgrid.ui.theme.SnapGridTheme
import com.snapgrid.viewmodel.AuthViewModel
import dagger.hilt.android.AndroidEntryPoint

@AndroidEntryPoint
class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContent {
            SnapGridTheme {
                val viewModel: AuthViewModel = hiltViewModel()
                val state by viewModel.state.collectAsState()
                MainNavigation(isLoggedIn = state.isLoggedIn)
            }
        }
    }
}