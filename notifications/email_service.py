import resend

resend.api_key = "re_ktZBhBXS_3eGfqhFGzmCduH6a9HoTLaEZ"

r = resend.Emails.send({
  "from": "onboarding@resend.dev",
  "to": "andersonnnnnn71@gmail.com",
  "subject": "Hello World",
  "html": "<p>Congrats on sending your <strong>first email</strong>!</p>"
})
