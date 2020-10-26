## No

Points: 50

At first glance, it looked like there was some stego is going on with the
image. After extracting the image using `pdfimages` and running it through some
tools, I couldn't find anything. I then decided to analyze the PDF a little
more closely. As I slowly scrolled through the output of `strings No.pdf`, I
found: `You looking for something?` followed by
`ZmxhZ3tUb3JvbnRvc1ByZXR0eUNvb2xFaD99`. This seemed to be a Base 64 encoded
string. After decoding it using `echo ZmxhZ3tUb3JvbnRvc1ByZXR0eUNvb2xFaD99 |
base64 -d`, I got `flag{TorontosPrettyCoolEh?}`
