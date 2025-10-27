document.addEventListener('DOMContentLoaded', function () {
    const phone = getCookie('phone');
    // 優先從 localStorage 取得 route1_questions_{market}
    let questions = [];
    let market = localStorage.getItem('route1_market') || '';
    if (market) {
        try {
            questions = JSON.parse(localStorage.getItem('route1_questions_' + market)) || [];
        } catch { questions = []; }
    }

    const contentDiv = document.querySelector('.content');
    if (questions.length > 0) {
        // 題號排序（由小到大）
        questions = questions.slice().sort((a, b) => parseInt(a.number) - parseInt(b.number));
        // 依據題目動態產生 6 個按鈕
        questions.forEach((q, idx) => {
            const buttonContainer = document.createElement('div');
            buttonContainer.classList.add('button-container');

            const button = document.createElement('button');
            button.dataset.level = q.number;
            // 圖片路徑統一改為 frontend/media/vendor_icons/題號.png
            button.style.backgroundImage = `url(./media/vendor_icons/${q.number}.png)`;

            const statusPassElement = document.createElement('div');
            statusPassElement.classList.add('status-pass');
            statusPassElement.id = `status${q.number}`;

            const statusFailElement = document.createElement('div');
            statusFailElement.classList.add('status-fail');
            statusFailElement.id = `fail${q.number}`;

            buttonContainer.appendChild(button);
            buttonContainer.appendChild(statusPassElement);
            buttonContainer.appendChild(statusFailElement);
            contentDiv.appendChild(buttonContainer);
        });
        // 狀態顯示
        if (phone) {
            fetch(postDetailUrl+phone)
                .then(response => response.json())
                .then(data => {
                    // 修正：content2 新結構
                    let content2 = data.content;
                    let content2Data = content2 && content2.data ? content2.data : content2;
                    let market = content2 && content2.market ? content2.market : '';
                    // 可在此 console.log 市集名稱
                    console.log('[route1] 所屬市集:', market);
                    questions.forEach(q => {
                        const statusPassElement = document.getElementById(`status${q.number}`);
                        const statusFailElement = document.getElementById(`fail${q.number}`);
                        const button = document.querySelector(`button[data-level="${q.number}"]`);
                        const status = content2Data[q.number.toString()]?.status;
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
    } else {
        // fallback: 沒有 localStorage 則用原本寫死的
        const levels = [6, 7, 8, 9, 10, 11];
        const buttonImages = {
            6: './media/vendor_icons/6.png',
            7: './media/vendor_icons/7.png',
            8: './media/vendor_icons/8.png',
            9: './media/vendor_icons/9.png',
            10: './media/vendor_icons/10.png',
            11: './media/vendor_icons/11.png',
        };
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
            buttonContainer.appendChild(button);
            buttonContainer.appendChild(statusPassElement);
            buttonContainer.appendChild(statusFailElement);
            contentDiv.appendChild(buttonContainer);
        });
        if (phone) {
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