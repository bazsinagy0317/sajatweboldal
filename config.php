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
    // Ha a nagybalazsweb.com hitelesítve lett: 'noreply@nagybalazsweb.com'
    'mail_from' => 'onboarding@resend.dev',

    // Ide érkeznek az űrlapról jövő üzenetek.
    'mail_to' => 'bazsinagy0317@gmail.com',

    // Küldjön-e automatikus visszaigazolást az érdeklődőnek?
    // Csak akkor működik, ha a feladó domain hitelesítve van a Resendben —
    // az onboarding@resend.dev teszt címről csak a saját fiókod címére lehet küldeni.
    'visszaigazolas' => false,

    // ── Süti nélküli látogatottság-mérés ──
    // true: gyűjti a napi összesítést az adatok/ mappába (IP-t nem tárol)
    'stat_be' => true,
    // Jelszó a statisztika.php megnyitásához (felhasználónevet hagyd üresen)
    'stat_jelszo' => 'IDE_JON_EGY_JELSZO',
];
