function showForm(action) {
    document.getElementById('form-add').style.display = 'none';
    document.getElementById('form-update').style.display = 'none';
    document.getElementById('form-search').style.display = 'none';
    if (action === 'add') {
        document.getElementById('form-add').style.display = 'block';
    } else if (action === 'update') {
        document.getElementById('form-update').style.display = 'block';
    } else if (action === 'search') {
        document.getElementById('form-search').style.display = 'block';
    }
}

function deleteSelected() {
    var form = document.createElement('form');
    form.method = 'post';
    form.action = '/administrator';
    var inputAction = document.createElement('input');
    inputAction.type = 'hidden';
    inputAction.name = 'action';
    inputAction.value = 'delete';
    form.appendChild(inputAction);
    document.querySelectorAll('input[name="selected_admins"]:checked').forEach(function (checkbox) {
        var input = document.createElement('input');
        input.type = 'hidden';
        input.name = 'selected_admins';
        input.value = checkbox.value;
        form.appendChild(input);
    });
    document.body.appendChild(form);
    form.submit();
}

function toggleAll(source) {
    checkboxes = document.querySelectorAll('.row-check');
    for (var i = 0; i < checkboxes.length; i++) {
        checkboxes[i].checked = source.checked;
    }
}

function showResultPopup(message) {
    if (message) {
        var popup = document.getElementById('popup');
        popup.textContent = "操作结果: " + message;
        popup.style.display = 'block';
        setTimeout(function () {
            popup.style.display = 'none';
        }, 3000);
        return false;
    }
    return true;
}

function submitForm(formId) {
    const form = document.getElementById(formId);
    fetch(form.action, {
        method: form.method,
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        showResultPopup(data.result);
        if (data.success) {
            location.reload(); // 如果操作成功，刷新页面以更新表格
        }
    })
    .catch(error => console.error('Error:', error));
    return false; // 阻止表单默认提交
}
