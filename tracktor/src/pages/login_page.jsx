import { use, useState } from "react";
import { Textbox } from "../components/Textbox";
import { Button } from "../components/Button";
import { useNavigate } from "react-router-dom";
import axios from "axios";

export function LoginPage() {

    const [successMsg, setSuccessMsg] = useState(""); 
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
            setSuccessMsg("User successfully created!")
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
        <div className="flex items-center justify-center min-h-screen bg-amber-50" >
            <div className="bg-white shadow-lg rounded-lg p-8 w-full max-w-md" >
                <h1 className="text-3xl font-extrabold mb-6 text-center text-amber-700 drop-shadow">VFX Production Tracker</h1>
                {successMsg && (
                    <div style={{
                        background: "#d1fae5",
                        color: "#065f46",
                        padding: "10px",
                        borderRadius: "5px",
                        marginBottom: "10px"
                    }}>
                        {successMsg}
                    </div>
                )}
                <label className="flex items-center justify-center">
                    Username:
                    <Textbox className={"bg-gray-200 ml-2 rounded"} 
                    value={username}
                    onChange={(e) => setUsername(e.target.value)}/>
                </label>
                <br></br>
                <label className="flex items-center justify-center">
                    Password:
                    <Textbox className={"bg-gray-200 ml-2 rounded"}
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}/>
                </label>
                <br></br>
                    <div className="flex justify-center flex-row gap-3">
                        <Button className="mb-2 bg-amber-300 text-amber-800 px-4 py-2 rounded" title={"Log in"} onClick={LoginUser}/>
                        <Button className="mb-2 bg-amber-300 text-amber-800 px-4 py-2 rounded" title={"Sign up"} onClick={CreateUser}/>
                    </div>
            </div>
        </div>
    )
}