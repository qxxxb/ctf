// cart logic
$('#toast-form').submit(function (event) {
    var sec = $("#toast-time").val()
    $.post("/api/toast", {"token": "gSNEaD868LJd1DldhZUglykfGwu_NbcLu9d1wmT5luLFTfHV2eVQYI8EupRMi71Cz6qydOc0kgXnGcDoPuUkkA", "time": sec}).done(function (data) {
        if (data.status == 0) {
            M.toast({html: data.message})
        }
    }).fail(function (xhr) {
        let data = JSON.parse(xhr.responseText);
        M.toast({html: data.error})
    })
})

