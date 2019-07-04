import React from 'react';
import {BrowserRouter as Router} from 'react-router-dom';

import axios from './axios';
import LoginChecker from './components/LoginChecker';

export const UserContext = React.createContext(null);

class App extends React.Component {
    constructor(props) {
        super(props);

        this.login = data => {
            const {access, refresh, user} = data;
            localStorage.setItem('token', access);
            localStorage.setItem('refresh-token', refresh);
            this.setState({
                loggedIn: true,
                user,
            });
        };

        this.logout = () => {
            this.setState({
                loggedIn: false,
                user: null
            });
            localStorage.removeItem("token");
            localStorage.removeItem("refresh-token");
        };

        this.state = {
            loggedIn: false,
            user: null,
            login: this.login,
            logout: this.logout
        };

        // add authorization header to every request
        axios.interceptors.request.use(config => {
            const token = localStorage.getItem('token');
            if (token) {
                config.headers.Authorization = `Bearer ${token}`;
            } else if (this.state.loggedIn) {
                this.logout()
            }
            return config;
        });

        // if 401 and both token and refresh token try getting new access token
        axios.interceptors.response.use(
            async response => response,
            async (error) => {
                const token = localStorage.getItem('token');
                const refreshToken = localStorage.getItem('refresh-token');
                if (error.response.status === 401) {
                    if (token && refreshToken) {
                        try {
                            const {data: {access}} = await axios.post(
                                'users/token/refresh/', {'refresh': refreshToken});
                            localStorage.setItem('token', access);
                            localStorage.removeItem('refresh-token');
                        } catch {
                            this.logout();
                        }
                    } else if (this.state.loggedIn) {
                        this.logout();
                    }
                }
                return Promise.reject(error);
            });
    }

    render() {
        return (
                <UserContext.Provider value={this.state}>
                <Router>
                <LoginChecker />
                </Router>
                </UserContext.Provider>
        );
    }
}

export default App;
