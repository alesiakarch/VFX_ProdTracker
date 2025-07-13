import { use, useState } from "react";
import { Textbox } from "../components/Textbox";
import { Button } from "../components/Button";
import { useNavigate } from "react-router-dom";

export function LoginPage() {


    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");
    const navigate = useNavigate()

    async function TakeToProjects() {
        navigate("/usernames-projects")
        
    }

    async function CreateUser() {
        
    }

    return (
        <div>
            <h1>Titles of the page</h1>
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
            <Button title={"Log in"} onClick={TakeToProjects}/>
            <Button title={"Sign up"} onClick={CreateUser}/>
        </div>
    )
}