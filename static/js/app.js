// Base url
const baseUrl = 'http://localhost:8000'

var table;
var title = $('#book-title');
var author = $('#book-author');
var publication_date = $('#book-publication-date');
var isbn = $('#book-isbn');
var book_id;
var action_add = true;
var username;

// Get book when my book page is loaded
$('#my-book-container').ready(function () {
    table = $('#myTable').DataTable({
        responsive: {
            details: {
                renderer: function (api, rowIdx, columns) {
                    var data = $.map(columns, function (col, i) {
                        return col.hidden ?
                            '<tr data-dt-row="' + col.rowIndex + '" data-dt-column="' + col.columnIndex + '">' +
                            '<td>' + col.title + ':' + '</td> ' +
                            '<td' + (col.title === 'Edit' ? ' class="td-buttons"' : '') + '>' + col.data + '</td>' +
                            '</tr>' :
                            '';
                    }).join('');

                    return data ?
                        $('<table/>').append(data) :
                        false;
                }
            }
        },
        ajax: { url: `${baseUrl}/books/all`, dataSrc: "" },
        columns: [
            { data: 'title' },
            { data: 'author' },
            { data: 'isbn' },
            { data: 'publication_date' },
            {
                data: null,
                defaultContent: '<button id="tbl-edit-btn" data-bs-toggle="modal" data-bs-target="#book-modal" class="btn btn-primary">Edit</button><button id="tbl-delete-btn" data-bs-toggle="modal" data-bs-target="#delete-modal" class="btn btn-danger ml2">Delete</button>',
                targets: -1
            }
        ],
        dom: 'Bfrtip',
        buttons: [
            {
                text: 'Add Book',
                action: function (e, dt, node, config) {
                    console.log("clied");
                    title.val('');
                    author.val('');
                    publication_date.val('');
                    isbn.val('');
                    action_add = true;
                    $('#book-modal').modal('toggle');
                }
            }
        ],
    });

    $('#myTable tbody').on('click', '#tbl-edit-btn', function (e) {
        let data = table.row(e.target.closest('tr')).data();
        console.log(data);
        title.val(data.title);
        author.val(data.author);
        publication_date.val(data.publication_date);
        isbn.val(data.isbn);
        book_id = data.id;
        action_add = false;
    });

    table.on('click', '#tbl-delete-btn', function (e) {
        let data = table.row(e.target.closest('tr')).data();
        book_id = data.id;
    });
});

// Submit POST or PUT request on book after editing/Adding on UI
// Same modal is used
$('#book-modal-btn').click((evt) => {
    evt.preventDefault();

    // TODO: Add cover photo upload
    // var file = $('#book-cover')[0].files[0];

    var payload = JSON.stringify({
        'title': title.val(),
        'author': author.val(),
        'publication_date': publication_date.val(),
        'isbn': isbn.val(),
    });

    $.ajax({
        url: action_add ? `${baseUrl}/books/create-book` : `${baseUrl}/books/update/${book_id}`,
        type: action_add ? 'POST' : 'PUT',
        contentType: "application/json; charset=utf-8",
        data: payload,
        success: (response) => {
            $('#book-modal').modal('toggle');
            table.ajax.reload();
        },
        error: (error) => {
            setAlert(error);
        }
    });
});


// Submit DELETE request on book after click on delete btn
$('#book-delete-btn').click((evt) => {
    evt.preventDefault();
    $.ajax({
        url: `${baseUrl}/books/delete/${book_id}`,
        type: 'DELETE',
        contentType: "application/json; charset=utf-8",
        success: (response) => {
            $('#delete-modal').modal('toggle');
            table.ajax.reload();
        },
        error: (error) => {
            setAlert(error);
        }
    });
});


// Get user data when account page is loaded
$('#my-profile-container').ready(function () {
    if (document.location.href === `${baseUrl}/user/`) {
        $.ajax({
            url: `${baseUrl}/users/`,
            type: 'GET',
            contentType: "application/json; charset=utf-8",
            success: (response) => {
                console.log(response);
                username = response.username;
                $('#account-username').append(response.username);
                $('#account-email').append(response.email);
            },
            error: (error) => {
                setAlert(error);
            }
        });
    }
});


// Submit PUT request on user after editing on UI
$('#profile-modal-btn').click((evt) => {
    evt.preventDefault();
    var payload = JSON.stringify({
        'username': username,
        'email': $('#account-email-form').val(),
    });

    console.log(payload);
    $.ajax({
        url: `${baseUrl}/users/`,
        type: 'PUT',
        data: payload,
        contentType: "application/json; charset=utf-8",
        success: (response) => {
            $('#profile-modal').modal('toggle');
            $('#account-email').empty();
            $('#account-email').append(response.email);
        },
        error: (error) => {
            setAlert(error);
        }
    });
});


// Get Book summary when dashboard page is loaded
$('#dashboard-container').ready(function () {

    $.ajax({
        url: `${baseUrl}/books/summary`,
        type: 'GET',
        contentType: "application/json; charset=utf-8",
        success: (response) => {
            console.log(response);
            $('#display-total-books').html(response.count);

            $('#recent-table').DataTable({
                responsive: true,
                data: response.books,
                columns: [
                    { data: 'title' },
                    { data: 'author' },
                    { data: 'isbn' },
                    { data: 'publication_date' },
                ],
            });
        },
        error: (error) => {
            setAlert(error);
        }
    });
});


// util function show alert when error occured
// Browser in-built alert used
// TODO: Make own alert service
function setAlert(msg) {
    console.log(msg);
    if (msg !== undefined) {
        msg = $.parseJSON(msg.responseText);
        let text = '';
        if (msg.detail) {
            if (Array.isArray(msg.detail)) {
                msg.detail.forEach(element => {
                    text = text + `* ${element.msg}`;
                });
            } else {
                text = `* ${msg.detail}`;
            }
        } else {
            text = `Error occured`;
        }
        console.log(text);
        alert(text);
    }
}
