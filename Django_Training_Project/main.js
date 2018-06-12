if (!document.onwheel) {
    var menu = document.querySelectorAll("div#menuContent.container");
    console.log(menu);
    if (menu.offsetWidth < 182 && menu !== null) {
        menu.style.display = 'None';
    }
}