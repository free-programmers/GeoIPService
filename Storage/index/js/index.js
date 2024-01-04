const burgerMenu = document.querySelector("#navbar-burger-menu")

const burgerMenuLine1 = document.querySelector(".line1")
const burgerMenuLine2 = document.querySelector(".line2")
const burgerMenuLine3 = document.querySelector(".line3")

burgerMenu.addEventListener("click", (e) => {
    burgerMenuLine2.classList.toggle("hide")
    burgerMenuLine1.classList.toggle("active")
    burgerMenuLine3.classList.toggle("active")
})