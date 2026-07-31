<?php
/**
 * Egyszerű, jelszóval védett statisztika-nézet.
 * A jelszó a config.php-ben van (stat_jelszo).
 */
declare(strict_types=1);

$cfg = @include __DIR__ . '/config.php';
$jelszo = is_array($cfg) ? (string)($cfg['stat_jelszo'] ?? '') : '';

if ($jelszo === '' || $jelszo === 'IDE_JON_EGY_JELSZO') {
    http_response_code(503);
    exit('A statisztika nincs beállítva. Adj meg egy jelszót a config.php stat_jelszo mezőjében.');
}
$megadott = (string)($_SERVER['PHP_AUTH_PW'] ?? '');
if (!hash_equals($jelszo, $megadott)) {
    header('WWW-Authenticate: Basic realm="Statisztika", charset="UTF-8"');
    http_response_code(401);
    exit('Belépés szükséges.');
}

$dir = __DIR__ . '/adatok';
$napok = [];
foreach (glob($dir . '/stat-*.json') ?: [] as $f) {
    $d = json_decode((string)file_get_contents($f), true);
    if (is_array($d)) { $napok[$d['nap'] ?? basename($f)] = $d; }
}
krsort($napok);

$osszMegt = 0; $osszLat = 0; $oldalak = []; $hivatkozok = []; $eszkozok = [];
foreach ($napok as $d) {
    $osszMegt += (int)($d['megtekintes'] ?? 0);
    $osszLat  += count($d['latogatok'] ?? []);
    foreach (($d['oldalak'] ?? []) as $k => $v)    { $oldalak[$k] = ($oldalak[$k] ?? 0) + $v; }
    foreach (($d['hivatkozok'] ?? []) as $k => $v) { $hivatkozok[$k] = ($hivatkozok[$k] ?? 0) + $v; }
    foreach (($d['eszkozok'] ?? []) as $k => $v)   { $eszkozok[$k] = ($eszkozok[$k] ?? 0) + $v; }
}
arsort($oldalak); arsort($hivatkozok); arsort($eszkozok);
$e = fn($s) => htmlspecialchars((string)$s, ENT_QUOTES | ENT_SUBSTITUTE, 'UTF-8');
$sor = function(array $a, int $n = 12) use ($e): string {
    $ki = ''; $i = 0;
    foreach ($a as $k => $v) {
        if ($i++ >= $n) break;
        $ki .= '<tr><td>' . $e($k) . '</td><td class="r">' . (int)$v . '</td></tr>';
    }
    return $ki ?: '<tr><td colspan="2">Még nincs adat.</td></tr>';
};
?><!DOCTYPE html>
<html lang="hu"><head><meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="robots" content="noindex,nofollow">
<title>Statisztika — Nagy Balázs</title>
<style>
*{margin:0;padding:0;box-sizing:border-box}
:root{--bg:#141210;--panel:#1C1917;--fg:#EFEAE2;--dim:#8A8078;--dim2:#A79E95;--acc:#C4471F;--line:rgba(239,234,226,.12)}
body{background:var(--bg);color:var(--fg);font-family:system-ui,-apple-system,Segoe UI,Roboto,sans-serif;line-height:1.6;padding:32px 20px 60px}
.wrap{max-width:900px;margin:0 auto}
h1{font-size:28px;font-weight:600;letter-spacing:-.03em;text-transform:uppercase;margin-bottom:6px}
.sub{color:var(--dim2);font-size:14px;font-weight:300;margin-bottom:26px}
.tops{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:1px;background:var(--line);border:1px solid var(--line);margin-bottom:26px}
.t{background:var(--panel);padding:20px}
.t .n{font-size:30px;font-weight:600;letter-spacing:-.03em;color:var(--acc);line-height:1}
.t .l{font-size:11px;letter-spacing:.12em;text-transform:uppercase;color:var(--dim);margin-top:8px}
h2{font-size:12px;letter-spacing:.14em;text-transform:uppercase;color:var(--acc);margin:26px 0 10px;font-weight:500}
table{width:100%;border-collapse:collapse;border:1px solid var(--line);font-size:13.5px}
td,th{padding:10px 14px;border-bottom:1px solid rgba(239,234,226,.06);color:var(--dim2);font-weight:300;text-align:left}
th{background:var(--panel);color:var(--dim);font-size:11px;letter-spacing:.12em;text-transform:uppercase}
.r{text-align:right;color:var(--fg);font-variant-numeric:tabular-nums}
tr:last-child td{border-bottom:none}
.note{margin-top:26px;border:1px solid var(--line);background:var(--panel);padding:18px 20px;font-size:13px;color:var(--dim2);font-weight:300}
</style></head><body><div class="wrap">
<h1>Látogatottság</h1>
<p class="sub">Süti nélküli mérés — nem tárol IP-címet, és nem tesz semmit a látogatók gépére.</p>
<div class="tops">
  <div class="t"><div class="n"><?= $osszMegt ?></div><div class="l">Oldalmegtekintés</div></div>
  <div class="t"><div class="n"><?= $osszLat ?></div><div class="l">Látogató (becsült)</div></div>
  <div class="t"><div class="n"><?= count($napok) ?></div><div class="l">Mért nap</div></div>
</div>
<h2>Napok</h2>
<table><tr><th>Nap</th><th class="r">Megtekintés</th><th class="r">Látogató</th></tr>
<?php $i=0; foreach ($napok as $nap => $d) { if ($i++>=30) break; ?>
<tr><td><?= $e($nap) ?></td><td class="r"><?= (int)($d['megtekintes'] ?? 0) ?></td><td class="r"><?= count($d['latogatok'] ?? []) ?></td></tr>
<?php } if (!$napok) { echo '<tr><td colspan="3">Még nincs adat.</td></tr>'; } ?>
</table>
<h2>Oldalak</h2><table><tr><th>Útvonal</th><th class="r">Megtekintés</th></tr><?= $sor($oldalak) ?></table>
<h2>Honnan érkeztek</h2><table><tr><th>Forrás</th><th class="r">Megtekintés</th></tr><?= $sor($hivatkozok) ?></table>
<h2>Eszközök</h2><table><tr><th>Típus</th><th class="r">Megtekintés</th></tr><?= $sor($eszkozok) ?></table>
<div class="note">A „látogató" becsült érték: naponta cserélődő, visszafejthetetlen lenyomat alapján számolt egyedi eszközszám.
Napokon átívelő követésre nem alkalmas, ezért ha valaki két napon is visszatér, két látogatónak számít.</div>
</div></body></html>
