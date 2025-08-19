import { Link, useLocation } from "react-router-dom";
import { ChevronsRight } from "lucide-react";

const validRoutes = [
  "/",
  "/:username/projects",
  "/:username/projects/join",
  "/:username/projects/create_project",
  "/:username/projects/:projectId",
  "/:username/projects/:projectId/share",
  "/:username/projects/:projectId/:itemType/:itemId",
  "/:username/projects/:projectId/:itemType/:itemId/notes",

];

function isValidRoute(path) {
  return validRoutes.some((route) => {
    const pattern = "^" + route.replace(/:[^/]+/g, "[^/]+") + "$";
    return new RegExp(pattern).test(path);
  });
}

export default function Breadcrumbs() {
  const location = useLocation();
  const pathnames = location.pathname.split("/").filter((x) => x);

  return (
    <nav className="flex items-center text-sm text-gray-500 my-4" aria-label="Breadcrumb">
      <Link to="/" className="hover:text-amber-700 font-semibold transition-colors">
        Home
      </Link>
      {pathnames.map((segment, index) => {
        const to = `/${pathnames.slice(0, index + 1).join("/")}`;
        const label = segment.charAt(0).toUpperCase() + segment.slice(1);
        const isValid = isValidRoute(to);
        const isLast = index === pathnames.length - 1;

        return (
          <span key={to} className="flex items-center">
            <ChevronsRight size={14} className="mx-2 text-gray-400" />
            {isValid && !isLast ? (
              <Link to={to} className="hover:text-amber-700 transition-colors">
                {label}
              </Link>
            ) : (
              <span className="text-gray-700 font-semibold">{label}</span>
            )}
          </span>
        );
      })}
    </nav>
  );
}