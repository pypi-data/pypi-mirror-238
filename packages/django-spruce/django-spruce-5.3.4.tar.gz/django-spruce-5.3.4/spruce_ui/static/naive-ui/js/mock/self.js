export function fotmat_input(type,name,value) {
    let nameInput = document.createElement("input");
    nameInput.type = type
    nameInput.name = name
    nameInput.value = value;
    return nameInput
}