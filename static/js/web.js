$(document).ready(function () {
    $('#datatable').DataTable();
})

function DeleteMessage() {
    const messages = document.getElementsByClassName("message");
    Array.from(messages).forEach(function(div) {
        div.remove();
    });
}