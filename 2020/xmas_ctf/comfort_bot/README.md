# Comfort Bot

**Category**: Web explotation \
**Points**: 432 \
**Author**: Milkdrop

## Challenge

This year has been a tough biscuit for everyone here in Lapland. Thankfully,
the inventive gnome engineers here have built a Comfort Bot that comforts
people! It might not offer thoughtful conversations, but it certainly is a good
listener... The gnomes made it available on the official X-MAS CTF Discord
server! How convenient. The bot is called: **Comfort Bot#7245**. You wouldn't break
it... would you? Note: flag is at `localhost/flag`

File: `bot.zip`

## Solution

Among other functionality, this bot likes respond with clever responses. It
out-sources this to [cleverbot.com](https://www.cleverbot.com/).

The responsible file is `responseEngines/cleverbot/driver.py`.

```python
def createCleverDriver ():
	global driver

	print("create1")
	chrome_options = Options()
	chrome_options.add_argument ("--headless")
	chrome_options.add_argument ("--no-sandbox")
	chrome_options.add_argument ("--disable-dev-shm-usage")
	chrome_options.binary_location = "/usr/bin/chromium"
	driver = webdriver.Chrome (executable_path = "/chall/chromedriver", options = chrome_options)
	print("create2")

...

async def getCleverResponse (authorID, txt):
	global driver

	try:
		driver.execute_script("window.open('http://localhost/','_blank');")
		windows[authorID] = driver.window_handles[-1]
		switchToAuthorWindow(authorID)

		script = "cleverbot.sendAI('{0}')".format (txt)
		driver.execute_script (script)
		while (driver.execute_script ("return cleverbot.aistate") != 0):
			await asyncio.sleep (0.4)
			switchToAuthorWindow(authorID)

		reply = driver.execute_script ("return cleverbot.reply")
		switchToAuthorWindow(authorID)
		driver.execute_script("window.close()")
		driver.switch_to_window(driver.window_handles[0])
		return reply
	except:
		CreateCleverDriver ()
```

So basically they're using a headless Chromium instance and sending it
JavaScript commands to:
- Open a new tab to a local instance of `cleverbot.com`
- Request a response using `cleverbot.sendAI()`
- Get the response in `cleverbot.reply()`

You can test these `cleverbot` commands on
[cleverbot.com](https://www.cleverbot.com/) and they indeed work.

Anyway, the vulnerability here is this line:
```python
script = "cleverbot.sendAI('{0}')".format (txt)
```

We control `txt` and the program doesn't sanitize it, so we can inject
JavaScript. Here's the plan:
1. Send a HTTP request to `localhost/flag`
2. Put the response in `cleverbot.reply`
3. Profit

![](w.png)
