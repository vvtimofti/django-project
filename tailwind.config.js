/** @type {import('tailwindcss').Config} */
module.exports = {
    content: [
        "./templates/*.html",
        "./templates/*/*.html",
        "./templates/*/*/*.html",
        "./apps/*/*.py",
    ],
    theme: {
        extend: {},
    },
    plugins: [require("daisyui")],
    daisyui: {
        themes: [
            "light",
            "dark",
            "cmyk",
            "pastel",
            "night",
            "sunset",
            "retro",
            "dim",
            "nord",
            "dracula",
        ],
    },
};
