const menus = document.querySelectorAll(".menu-title");

menus.forEach(menu => {

    menu.addEventListener("click", () => {

        const submenu = menu.nextElementSibling;

        if (submenu) {

            if (submenu.style.display === "block") {
                submenu.style.display = "none";
            } else {
                submenu.style.display = "block";
            }

        }

    });

});