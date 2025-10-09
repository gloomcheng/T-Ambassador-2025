// 修改區開始-----------------------------------------------------------------------------------------------------
// 只有一處要修改(整條一起修改)

var routes = [
    { url: "route1.html", action: "Toroute1Page", image: "./media/vendor_icons/button_1.png" },
    { url: "route1.html", action: "Toroute1Page", image: "./media/vendor_icons/button_1.png" },
    { url: "route1.html", action: "Toroute1Page", image: "./media/vendor_icons/button_1.png" },
    { url: "route1.html", action: "Toroute1Page", image: "./media/vendor_icons/button_1.png" },
    // { url: "route3.html", action: "Toroute3Page", image: "./media/vendor_icons/button_3.png" },多一條就多一個按鈕
];

// 修改區結束-----------------------------------------------------------------------------------------------------









// 不要更改的區塊----------------------------------------------------------------------------------------------------

// 動態創建函數
routes.forEach((route, index) => {
    window[`Toroute${index + 1}Page`] = function() {
        window.location.href = route.url;
    };
});

// 動態生成按鈕
document.addEventListener('DOMContentLoaded', function() {
    const container = document.querySelector('.btr');
    
    routes.forEach((route, index) => {
        const button = document.createElement('button');
        button.className = `button0`;
        // button.className = `button${index + 1} button0`;
        button.style.backgroundImage = `url(${route.image})`;
        button.onclick = window[`Toroute${index + 1}Page`];
        container.appendChild(button);
    });
});

