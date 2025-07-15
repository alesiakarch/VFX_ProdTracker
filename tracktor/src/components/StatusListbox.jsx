import { Listbox, ListboxButton, ListboxOption, ListboxOptions } from "@headlessui/react";


export function StatusListbox({ value, onChange}) {
        const listboxOptions = ["Not started", "WIP", "Ready to Review", "Complete"]
    return (
        <Listbox value={value} onChange={onChange}>
            <ListboxButton>{value}</ListboxButton>
            <ListboxOptions>
                {listboxOptions.map(option => (
                    <ListboxOption key={option} value={option}>{option}</ListboxOption>
                ))}
            </ListboxOptions>

        </Listbox>
    )
}