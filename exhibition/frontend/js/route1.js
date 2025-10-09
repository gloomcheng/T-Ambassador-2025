document.addEventListener('DOMContentLoaded', function () {
    const phone = getCookie('phone');

// 修改區開始------------------------------------------------------------------------------------
//一個關卡有兩處要修改

    const levels = [6, 7, 8, 9, 10, 11];  // 1.設定關卡編號
    const buttonImages = {
        //2.設定關卡圖片
        6: './media/vendor_icons/6.png',
        7: './media/vendor_icons/7.png',
        8: './media/vendor_icons/8.png',
        9: './media/vendor_icons/9.png',
        10: './media/vendor_icons/10.png',
        11: './media/vendor_icons/11.png',
    };

    var postDetailUrl = "https://tdance.fansee.studio/trips/api/post-detail/";
// 修改區結束------------------------------------------------------------------------------------






    const contentDiv = document.querySelector('.content');

    // 生成按鈕
    levels.forEach(level => {
        const buttonContainer = document.createElement('div');
        buttonContainer.classList.add('button-container');

        const button = document.createElement('button');
        button.dataset.level = level;
        button.style.backgroundImage = `url(${buttonImages[level]})`;

        const statusPassElement = document.createElement('div');
        statusPassElement.classList.add('status-pass');
        statusPassElement.id = `status${level}`;

        const statusFailElement = document.createElement('div');
        statusFailElement.classList.add('status-fail');
        statusFailElement.id = `fail${level}`;

        // 將按鈕和狀態元素添加到容器
        buttonContainer.appendChild(button);
        buttonContainer.appendChild(statusPassElement);
        buttonContainer.appendChild(statusFailElement);

        // 將按鈕容器添加到頁面
        contentDiv.appendChild(buttonContainer);
    });

    if (phone) {
        // fetch(`https://tdance.fansee.studio/trips/api/post-detail/${phone}/`)
        fetch(postDetailUrl+phone)
            .then(response => response.json())
            .then(data => {
                levels.forEach(level => {
                    const statusPassElement = document.getElementById(`status${level}`);
                    const statusFailElement = document.getElementById(`fail${level}`);
                    const button = document.querySelector(`button[data-level="${level}"]`);

                    const status = data.content[level.toString()]?.status;
                    if (status === 'pass') {
                        button.disabled = true;
                        statusPassElement.style.display = 'block';
                    } else if (status === 'fail') {
                        button.disabled = true;
                        statusFailElement.style.display = 'block';
                    }
                });
            })
            .catch(error => {
                console.error('Error fetching post details', error);
            });
    }
});

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function handleButtonClick(level) {
    document.cookie = `level=${level}; path=/; max-age=${60 * 60 * 24 * 30}`; // 30 days
    window.location.href = `arScan00.html`;
    // window.location.href = `arScan${level}.html`;//多個掃描頁面時使用
}

document.addEventListener('click', function (event) {
    if (event.target.tagName === 'BUTTON' && event.target.dataset.level) {
        const level = event.target.dataset.level;
        handleButtonClick(level);
    }
});