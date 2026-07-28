import nodemailer from 'nodemailer';

// Sends through your own Gmail via SMTP + an App Password. Built here (not at
// import) so a missing config never breaks the build or an unrelated route.
function getTransport() {
  return nodemailer.createTransport({
    host: 'smtp.gmail.com',
    port: 465,
    secure: true,
    auth: {
      user: process.env.SMTP_USER,
      pass: process.env.SMTP_PASSWORD,
    },
  });
}

async function send(
  to: string,
  subject: string,
  heading: string,
  intro: string,
  buttonText: string,
  link: string,
) {
  const from = process.env.EMAIL_FROM!;
  const html = `
    <div style="font-family: Georgia, serif; max-width: 480px; margin: 0 auto; color: #2b2b2b;">
      <h2 style="font-weight: normal;">${heading}</h2>
      <p style="line-height: 1.5;">${intro}</p>
      <p style="margin: 28px 0;">
        <a href="${link}"
           style="background: #4b3b2f; color: #fff; padding: 12px 20px;
                  text-decoration: none; border-radius: 6px; display: inline-block;">
          ${buttonText}
        </a>
      </p>
      <p style="font-size: 13px; color: #777; line-height: 1.5;">
        Falls der Knopf nicht funktioniert, kopiere diesen Link in deinen Browser:<br>
        <span style="word-break: break-all;">${link}</span>
      </p>
      <p style="font-size: 13px; color: #777;">
        Wenn du das nicht angefordert hast, kannst du diese E-Mail ignorieren.
      </p>
    </div>
  `;

  await getTransport().sendMail({ from, to, subject, html });
}

/** Viewer signup: confirm the email address. */
export async function sendVerifyEmail(to: string, link: string) {
  await send(
    to,
    'Bestätige deine E-Mail-Adresse',
    'Willkommen bei Bibliopa',
    'Bitte bestätige deine E-Mail-Adresse, um dein Konto zu aktivieren.',
    'E-Mail bestätigen',
    link,
  );
}

/** Admin created a researcher/family account: they set their first password. */
export async function sendSetPasswordEmail(to: string, link: string) {
  await send(
    to,
    'Lege dein Passwort fest',
    'Dein Bibliopa-Konto ist bereit',
    'Für dich wurde ein Konto angelegt. Lege jetzt dein Passwort fest, um dich anzumelden.',
    'Passwort festlegen',
    link,
  );
}

/** Forgot password: set a new one. */
export async function sendResetEmail(to: string, link: string) {
  await send(
    to,
    'Passwort zurücksetzen',
    'Passwort zurücksetzen',
    'Du hast angefordert, dein Passwort zurückzusetzen. Lege hier ein neues Passwort fest.',
    'Neues Passwort festlegen',
    link,
  );
}
