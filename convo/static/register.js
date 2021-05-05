
const nameInput = document.querySelector('input[name=name]');
const userInput = document.querySelector('input[name=username]');

const slugify = (val) =>
{
    return val.toString().toLowerCase().trim()
        .replace(/&/g, '-and')         // Replace & with 'and'
        .replace(/[\s\W-]+/g, '-')     // Replace spaces, non-word characters and dashes with a single dash (-)
};

nameInput.addEventListener('keyup', (e) =>
{
userInput.value = slugify(nameInput.value);
});