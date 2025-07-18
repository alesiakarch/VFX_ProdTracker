import { Listbox, ListboxButton, ListboxOption, ListboxOptions } from "@headlessui/react";


export function StatusListbox({ value, onChange}) {
    const listboxOptions = ["Not started", "WIP", "Ready to Review", "Complete"]
    return (
        <Listbox value={value} onChange={onChange}>
            <ListboxButton className="bg-gray-100 border border-gray-300 rounded px-2 py-1 w-full text-left focus:outline-none focus:ring-2 focus:ring-amber-400">
                {value}
            </ListboxButton>
            <ListboxOptions className="bg-white border border-gray-300 justify-center rounded shadow-lg mt-1 absolute z-10">
                {listboxOptions.map(option => (
                    <ListboxOption key={option}
                                   value={option}
                                   className={({ isActive, isSelected }) =>
                                        `cursor-pointer  px-2 py-1 ${isActive ? "bg-amber-100" : ""} ${isSelected ? "font-bold" : ""}`
                                    }>
                                    {option}
                                   </ListboxOption>
                ))}
            </ListboxOptions>

        </Listbox>
    )
}