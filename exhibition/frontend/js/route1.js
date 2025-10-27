document.addEventListener('DOMContentLoaded', function () {
    const phone = getCookie('phone');
    let questions = [];
    let market = localStorage.getItem('route1_market') || '';
    if (market) {
        try {
            questions = JSON.parse(localStorage.getItem('route1_questions_' + market)) || [];
        } catch { questions = []; }
    }
    const contentDiv = document.querySelector('.content');

    function renderButtons(questionsOrLevels, isFallback) {
        contentDiv.innerHTML = '';
        questionsOrLevels.forEach(q => {
            const number = isFallback ? q : q.number;
            const buttonContainer = document.createElement('div');
            buttonContainer.classList.add('button-container');
            const button = document.createElement('button');
            button.dataset.level = number;
            button.style.backgroundImage = `url(./media/vendor_icons/${number}.png)`;
            const statusPassElement = document.createElement('div');
            statusPassElement.classList.add('status-pass');
            statusPassElement.id = `status${number}`;
            const statusFailElement = document.createElement('div');
            statusFailElement.classList.add('status-fail');
            statusFailElement.id = `fail${number}`;
            buttonContainer.appendChild(button);
            buttonContainer.appendChild(statusPassElement);
            buttonContainer.appendChild(statusFailElement);
            contentDiv.appendChild(buttonContainer);
        });
    }

    function refreshProgress() {
        if (questions.length > 0) {
            // 題號排序（由小到大）
            questions = questions.slice().sort((a, b) => parseInt(a.number) - parseInt(b.number));
            renderButtons(questions, false);
            if (phone) {
                fetch(postDetailUrl+phone)
                    .then(response => response.json())
                    .then(data => {
                        let content2 = data.content2;
                        let market = localStorage.getItem('route1_market') || '';
                        let content2Data = (content2 && content2[market] && content2[market]['data']) ? content2[market]['data'] : {};
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
            renderButtons(levels, true);
            if (phone) {
                fetch(postDetailUrl+phone)
                    .then(response => response.json())
                    .then(data => {
                        let content2 = data.content2;
                        let market = localStorage.getItem('route1_market') || '';
                        let content2Data = (content2 && content2[market] && content2[market]['data']) ? content2[market]['data'] : {};
                        levels.forEach(level => {
                            const statusPassElement = document.getElementById(`status${level}`);
                            const statusFailElement = document.getElementById(`fail${level}`);
                            const button = document.querySelector(`button[data-level="${level}"]`);
                            const status = content2Data[level.toString()]?.status;
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
    }

    // 頁面初次載入自動刷新一次
    refreshProgress();
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
    localStorage.setItem('route1_selected_level', level);
    window.location.href = `arScan00.html`;
    // window.location.href = `arScan${level}.html`;//多個掃描頁面時使用
}

document.addEventListener('click', function (event) {
    if (event.target.tagName === 'BUTTON' && event.target.dataset.level) {
        const level = event.target.dataset.level;
        handleButtonClick(level);
    }
});