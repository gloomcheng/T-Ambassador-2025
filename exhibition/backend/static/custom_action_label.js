document.addEventListener('DOMContentLoaded', function() {
    // 將 Action label 改為「動作」
    var labels = document.querySelectorAll('label');
    labels.forEach(function(label) {
        if (label.textContent.trim() === 'Action:') {
            label.textContent = '動作：';
        }
    });
    // 將下拉選單的刪除選項改為「刪除」
    var actionSelect = document.querySelector('select[name="action"]');
    if (actionSelect) {
        for (var i = 0; i < actionSelect.options.length; i++) {
            if (actionSelect.options[i].value === 'delete_selected') {
                actionSelect.options[i].text = '刪除';
            }
        }
    }
});
