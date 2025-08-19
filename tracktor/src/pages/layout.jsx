import Breadcrumbs from "../components/Breadcrumbs";
import { Navbar } from "../components/Navbar";
import { Outlet } from "react-router-dom";

export function Layout () {
    return (
        <>
            {/* <Navbar /> */}
            <Breadcrumbs />
            <main>
                <Outlet />
            </main>
        </>
    )
}