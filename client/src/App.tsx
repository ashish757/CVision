import {BrowserRouter, Routes, Route, Navigate} from "react-router-dom";
import {useSelector} from "react-redux";
import ProtectedRoute from "./components/ProtectedRoute";
import {useRefreshToken} from "./hooks/useRefreshToken.ts";
import type {RootState} from "./redux/store";
import type {ReactNode} from "react";
import {Landing, SignIn, SignUp, Dashboard, NotFound, Settings, Analytics, Analyse} from "./pages";


/**
 * Wrapper component for auth pages (sign in/sign up)
 * Redirects to dashboard if user is already authenticated
 */
const AuthRoute = ({children}: { children: ReactNode }) => {
    const isAuthenticated = useSelector(
        (state: RootState) => state.auth.isAuthenticated
    );

    if (isAuthenticated) {
        return <Navigate to="/dashboard" replace/>;
    }

    return <>{children}</>;
};

function App() {
    // Initialize authentication on app load
    useRefreshToken();

    return (
        <BrowserRouter>
            <Routes>
                <Route path="/" element={
                    <AuthRoute>
                        <Landing/>
                    </AuthRoute>
                }/>

                <Route
                    path="/signin"
                    element={
                        <AuthRoute>
                            <SignIn/>
                        </AuthRoute>
                    }
                />
                <Route
                    path="/signup"
                    element={
                        <AuthRoute>
                            <SignUp/>
                        </AuthRoute>
                    }
                />
                <Route
                    path="/dashboard"
                    element={
                        <ProtectedRoute>
                            <Dashboard/>
                        </ProtectedRoute>
                    }
                />
                <Route path="/analytics" element={
                    <ProtectedRoute>
                        <Analytics/>
                    </ProtectedRoute>
                }
                />
                <Route path="/analyse" element={
                    <ProtectedRoute>
                        <Analyse/>
                    </ProtectedRoute>
                }
                />
                <Route path="/settings" element={
                    <ProtectedRoute>
                        <Settings />
                    </ProtectedRoute>
                }
                />

                <Route path="*" element={<NotFound/>}/>
            </Routes>
        </BrowserRouter>
    );
}

export default App;

