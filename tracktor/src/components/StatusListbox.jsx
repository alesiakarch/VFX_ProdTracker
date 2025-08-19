import { Listbox, ListboxButton, ListboxOption, ListboxOptions } from "@headlessui/react";


export function StatusListbox({ value, onChange, colourMap = {} }) {
    const listboxOptions = ["Not started", "WIP", "Ready to Review", "Complete", "Omitted"];
    return (
        <Listbox value={value} onChange={onChange}>
            <ListboxButton
                className={`border border-gray-300 rounded px-2 py-1 w-full text-left focus:outline-none focus:ring-2 focus:ring-amber-400 transition-colors ${colourMap[value] || ""}`}
            >
                {value}
            </ListboxButton>
            <ListboxOptions className="bg-white border border-gray-300 rounded shadow-lg mt-1 absolute z-10">
                {listboxOptions.map(option => (
                    <ListboxOption
                        key={option}
                        value={option}
                        className="cursor-pointer px-2 py-1"
                    >
                        {option}
                    </ListboxOption>
                ))}
            </ListboxOptions>
        </Listbox>
    );
}