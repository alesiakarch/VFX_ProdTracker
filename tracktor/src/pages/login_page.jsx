import { use, useState } from "react";
import { Textbox } from "../components/Textbox";
import { Button } from "../components/Button";
import { useNavigate } from "react-router-dom";
import axios from "axios";

export function LoginPage() {


    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");
    const navigate = useNavigate()

    async function LoginUser() {
        if (!username.trim() || !password.trim()) {
            alert("Username and password cannot be empty!");
            return;
        }
        try{
            const response = await axios.post("http://localhost:8080/api/login", {
                                               user_name:username,
                                               user_password:password
                                            })
            if (response.data.success) {
                localStorage.setItem("user_id", response.data.user_id)
                navigate(`/${username}/projects`)
            } else {
                alert("Invalid username or password!")
            }
        } catch (error) {
            if (error.response) {
        // Backend responded with an error status (e.g., 401 Unauthorized)
                alert(error.response.data.error || "Login failed!");
            } else if (error.request) {
                // Request was made but no response received
                alert("No response from server. Please try again later.");
            } else {
                // Something else went wrong
                alert("An unexpected error occurred.");
            }
            console.error(error);
        }        
    }

    async function CreateUser() {
        if (!username.trim() || !password.trim()) {
            alert("Username and password cannot be empty!");
            return;
        }
        try{
            const response = await axios.post("http://localhost:8080/api/users", {
                                            user_name:username,
                                            user_password:password
                                        })
        } catch (error) {
             console.error("Axios error object:", error);
            if (error.response) {
                console.error("Axios error response:", error.response);
            }
            if (error.request) {
                console.error("Axios error request:", error.request);
            }
            if (error.message) {
                console.error("Axios error message:", error.message);
            }
            alert("Failed to create a new user")
        }
        
        
    }

    return (
        <div>
            <h1>VFX Production Tracker</h1>
            <label>
                Username:
                <Textbox className={"bg-gray-200"} 
                value={username}
                onChange={(e) => setUsername(e.target.value)}/>
            </label>
            <br></br>
            <label>
                Password:
                <Textbox className={"bg-gray-200"}
                 value={password}
                 onChange={(e) => setPassword(e.target.value)}/>
            </label>
            <br></br>
            <Button title={"Log in"} onClick={LoginUser}/>
            <Button title={"Sign up"} onClick={CreateUser}/>
        </div>
    )
}