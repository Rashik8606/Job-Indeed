
import {useContext} from 'react'
import jwtDecode from 'jwt-decode'; // Correct import
import { AuthContext } from '../context/AuthContext'; // Correct named import
import { Link } from 'react-router-dom'

function NavBar() {

  const {user, logoutUser} = useContext(AuthContext)
  const token = localStorage.getItem("authTokens")

  if (token){
    const decoded = jwtDecode(token) 
    var user_id = decoded.user_id
  }

  return (
    <div>
        <nav class="navbar navbar-expand-lg navbar-dark fixed-top bg-dark">
        <div class="container-fluid">
          <a class="navbar-brand" href="#">
            <img style={{width:"120px", padding:"6px"}} src="https://i.imgur.com/juL1aAc.png" alt="" />

          </a>
          <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
            <span class="navbar-toggler-icon"></span>
          </button>
          <div class="collapse navbar-collapse" id="navbarNav">
            <ul class="navbar-nav ">
              <li class="nav-item">
                <a class="nav-link active" aria-current="page" href="#"> <i className='fas fa-home'></i> Home</a>
              </li>
              {token === null && 
              <>
                <li class="nav-item">
                  <Link class="nav-link" to="/login"><i className='fas fa-sign-in-alt'></i> Login</Link>
                </li>
                <li class="nav-item">
                  <Link class="nav-link" to="/register"><i className='fas fa-user-plus'></i> Register</Link>
                </li>
              </>
              }

            {token !== null && 
              <>
                <li class="nav-item">
                  <Link class="nav-link" to="/dashboard"> <i className='fas fa-th'></i> Dashboard</Link>
                </li>
                <li class="nav-item">
                  <Link class="nav-link" to="/todo"> <i className='fas fa-pen'></i> Todo</Link>
                </li>
                <li class="nav-item">
                  <Link class="nav-link" to="/inbox"> <i className='fas fa-envelope'></i> Inbox</Link>
                </li>
                <li class="nav-item">
                  <a class="nav-link" onClick={logoutUser} style={{cursor:"pointer"}}> <i className='fas fa-sign-out-alt'></i>Logout</a>
                </li>
              </>
              }   
              
            </ul>
          </div>
        </div>
      </nav>
    </div>
  )
}

export default NavBar
