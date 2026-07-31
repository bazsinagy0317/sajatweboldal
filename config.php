<?php
/**
 * Titkos beállítások.
 * EZT A FÁJLT NE TEDD FEL GITHUBRA és ne oszd meg senkivel.
 * A .htaccess letiltja a közvetlen elérését.
 */
return [
    // A Resend API kulcsod (resend.com → API Keys → Create API Key)
    'resend_api_key' => 'IDE_JON_A_RESEND_KULCS',

    // Feladó cím.
    // Amíg nincs a domain hitelesítve a Resendben, marad az onboarding@resend.dev
    // (ez csak a saját Resend-fiókod e-mail címére tud küldeni — nekünk pont az kell).
    // Ha a DOMAIN.HU hitelesítve lett: 'noreply@DOMAIN.HU'
    'mail_from' => 'onboarding@resend.dev',

    // Ide érkeznek az űrlapról jövő üzenetek.
    'mail_to' => 'bazsinagy0317@gmail.com',
];
