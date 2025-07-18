

export function Button({title, onClick, className}) {
     const base =
        "transition-colors duration-200 hover:brightness-90 focus:outline-none focus:ring-2 focus:ring-amber-500";
    return (
        <button className = {`${base} ${className || ""}`} onClick={onClick}>
            {title} 
        </button>
    )
}