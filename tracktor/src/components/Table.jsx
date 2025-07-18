
export function Table({columns, rows}) {
    return (
        <div className="overflow-x-auto">
            <table className="min-w-full max-w-screen border border-gray-300 rounded-lg">
                <thead>
                    <tr className="bg-amber-100">
                        {columns.map((col) => (
                            <th key={col.key} className="px-4 py-2 text-left">{col.header}</th>
                        ))}
                    </tr>
                </thead>
                <tbody>
                    {rows.map((row, i) => (
                        <tr key={i} className={i % 2 === 0 ? "bg-white" : "bg-amber-50"}>
                            {columns.map((col) => (
                                <td key={col.key} className="px-4 py-2">
                                    {typeof col.render === "function"
                                    ? col.render(row[col.key], row)
                                    : row[col.key]}
                                </td>
                            ))}
                        </tr>
                    ))}
                </tbody>
            </table>
        </div>
    )
}