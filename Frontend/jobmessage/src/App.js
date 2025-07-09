import React from 'react'

import {BrowserRouter as Router, Route, Switch} from "react-router-dom"
import PrivateRoute from "./utils/PrivateRoute"
import { AuthProvider } from './context/AuthContext'

import HomePage from './views/HomePage'
import RegisterPage from './views/RegisterPage'
import LoginPage from './views/LoginPage'
import DashBoard from './views/DashBoard'
import NavBar from './views/NavBar'
import Message from './views/Message'
import MessageDetails from './views/MessageDetails';
import SearchUser from './views/SearchUser';



function App() {
  return (
    <Router>
      <AuthProvider>
        <NavBar/>
        <Switch>
          <PrivateRoute component={DashBoard} path="/dashboard" exact />
          <Route component={LoginPage} path="/login" />
          <Route component={RegisterPage} path="/register" exact />
          <Route component={HomePage} path="/" exact />
          <Route component={Message} path="/inbox" exact />
          <Route component={MessageDetails} path="/inbox/:id" exact />
          <Route component={SearchUser} path="/search/:username" exact />
        </Switch>
      </AuthProvider>
    </Router>
  )
}

export default App