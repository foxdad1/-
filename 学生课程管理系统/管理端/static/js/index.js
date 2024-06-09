document.addEventListener('DOMContentLoaded', function () {
    const links = document.querySelectorAll('.sidebar a');

    links.forEach(link => {
        link.addEventListener('click', function (event) {
            event.preventDefault();
            const url = this.getAttribute('href');
            const submenu = this.nextElementSibling;
            if (submenu && submenu.classList.contains('submenu')) {
                submenu.classList.toggle('active');
            } else {
                loadPage(url);
            }
        });
    });

    function loadPage(url) {
        const xhr = new XMLHttpRequest();
        xhr.onreadystatechange = function () {
            if (xhr.readyState === 4 && xhr.status === 200) {
                const iframe = document.querySelector('iframe[name="main"]');
                const doc = iframe.contentWindow.document;
                doc.open();
                doc.write(xhr.responseText);
                doc.close();
            }
        };
        xhr.open('GET', url, true);
        xhr.send();
    }

    //绑定表单
    const formActions = ["/administrator", "/grade", "/grade_infos", "/student", "/teacher", "/teacher_class", "/update_student"];

    formActions.forEach(action => {
        const form = document.querySelector(`form[action="${action}"]`);
        if (form) {
            form.addEventListener('submit', handleSubmit);
        }
    });

})