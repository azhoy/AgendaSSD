import { BrowserRouter as Router, Route, Routes} from 'react-router-dom'
import HomePage from "./pages/HomePage";
import LoginPage from "./pages/LoginPage";
import Header from "./components/Header";
import RequireAuth from "./utils/PrivateRoute";
import {AuthProvider} from "./context/AuthContext";
import EventPage from "./pages/EventPage";
import RegisterPage from "./pages/RegisterPage";
import {KeyProvider} from "./context/KeyContext";
import createEvent from "./pages/CreateEventPage";
import CreateEventPage from "./pages/CreateEventPage";
import ContactPage from "./pages/ContactPage";
function App() {
    return (
    <div className="App">

        <Router>
            <AuthProvider>
                <KeyProvider>
                    <Header></Header>
                    <Routes>
                        <Route element={<RequireAuth redirectTo='/login'>{<HomePage/>}</RequireAuth>} path="/" ></Route>
                        <Route element={<LoginPage/>} path="/login" ></Route>
                        <Route element={<RegisterPage/>} path="/register" ></Route>
                        <Route element={<RequireAuth redirectTo='/login'>{<EventPage/>}</RequireAuth>} path="/event" ></Route>
                        <Route element={<RequireAuth redirectTo='/login'>{<CreateEventPage/>}</RequireAuth>} path="/createEvent" ></Route>
                        <Route element={<RequireAuth redirectTo='/login'>{<ContactPage/>}</RequireAuth>} path="/contacts" ></Route>
                    </Routes>
                </KeyProvider>
            </AuthProvider>
        </Router>
    </div>
  )
}

export default App
