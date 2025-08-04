import { useState } from "react";
import { Button } from "./Button";

export function Popup({open, onClose, onSubmit, fields = []}) {
    const [data, setData] = useState({})

    if (!open) return null

    const handleChange = (e) => {
        setData({...data, [e.target.name]: e.target.value})
    }

    const handleSubmit = (e) => {
        e.preventDefault()
        onSubmit(data)
        setData({})
    }

    return (  
        <div className="fixed inset-0 flex items-center justify-center z-50"
             onClick={onClose}
        >
            <div className="bg-white rounded-lg shadow-lg p-6 min-w-[300px]"
                 onClick={e => e.stopPropagation()}
            >
                <form onSubmit={handleSubmit}>
                    {fields.map(field => (
                        <div key={field.name} className="mb-3">
                            <label className="block mb-1 font-medium">{field.label}</label>
                                <input
                                    type={field.type || "text"}
                                    name={field.name}
                                    value={data[field.name] || ""}
                                    onChange={handleChange}
                                    className="border rounded px-2 py-1 w-full"
                                    required={field.required}
                                />
                        </div>
                    ))}
                    <div className="flex gap=2 mt-2 justify-end">
                        <Button type="submit" title="Submit" className="bg-amber-300 text-white px-4 py-2 rounded mt-2"/>
                    </div>
                </form>
            </div>
        </div>
     )
}