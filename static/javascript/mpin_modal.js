document.addEventListener('DOMContentLoaded', function() {
    const modal = document.getElementById('myModal');
    const closeModalBtn = document.getElementsByClassName('close')[0];
    const mpinForm = document.getElementById('mpinForm');
    modal.style.display = 'block';
    closeModalBtn.addEventListener('click', function() {
        modal.style.display = 'none';
    });
    window.addEventListener('click', function(event) {
        if (event.target === modal) {
            modal.style.display = 'none';
        }
    });
});
