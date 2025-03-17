document.addEventListener("DOMContentLoaded", function () {
    const boton = document.querySelector(".boton-enviar");

    boton.addEventListener("mouseover", function (e) {
        const flor = this.querySelector(".flor");
        flor.style.top = `${e.offsetY}px`;
        flor.style.left = `${e.offsetX}px`;
    });
});

/*===============================================================
    esto es un aprueba para el paartado de tecnologias usasdas 
==============================================================*/

document.addEventListener("DOMContentLoaded", function () {
    const iconos = document.querySelectorAll(".icono-wow");

    iconos.forEach(icono => {
        let randomX = Math.random() * 4 - 2; // Movimiento horizontal aleatorio
        let randomY = Math.random() * 4 - 2; // Movimiento vertical aleatorio

        icono.style.animation = `flotacion ${3 + Math.random()}s infinite ease-in-out alternate`;

        icono.addEventListener("mouseover", () => {
            icono.style.transform = `scale(1.3) rotate(${randomX * 5}deg)`;
        });

        icono.addEventListener("mouseout", () => {
            icono.style.transform = `translate(${randomX}px, ${randomY}px) rotate(${randomX}deg)`;
        });
    });
});

