<?php
/**
 * Süti nélküli látogatottság-mérés
 * ---------------------------------
 * Nem tesz semmit a látogató gépére, és nem tárol IP-címet.
 * Az egyedi látogatók becsléséhez naponta cserélődő, véletlen "sóval"
 * képzett lenyomatot használ, amiből az eredeti adat nem állítható vissza.
 * A napi só éjfélkor érvényét veszti, így a lenyomat nem alkalmas
 * napokon átívelő követésre.
 */

declare(strict_types=1);

header('Content-Type: application/json; charset=utf-8');
header('X-Content-Type-Options: nosniff');

function vege(array $a, int $k = 200): never {
    http_response_code($k);
    echo json_encode($a, JSON_UNESCAPED_UNICODE);
    exit;
}

if (($_SERVER['REQUEST_METHOD'] ?? '') !== 'POST') {
    vege(['ok' => false], 405);
}

$cfg = @include __DIR__ . '/config.php';
if (!is_array($cfg) || empty($cfg['stat_be'])) {
    vege(['ok' => true]);           /* kikapcsolva — csendben nyugtázunk */
}

$dir = __DIR__ . '/adatok';
if (!is_dir($dir)) { @mkdir($dir, 0750, true); }
if (!is_dir($dir)) { vege(['ok' => false], 500); }

/* ── Napi só: éjfélkor cserélődik, nem visszafejthető ── */
$ma      = gmdate('Y-m-d');
$soFajl  = $dir . '/so.php';
$so      = null;
if (is_readable($soFajl)) {
    $t = @include $soFajl;
    if (is_array($t) && ($t['nap'] ?? '') === $ma) { $so = (string)$t['so']; }
}
if ($so === null) {
    $so = bin2hex(random_bytes(16));
    @file_put_contents($soFajl, "<?php return ['nap'=>'{$ma}','so'=>'{$so}'];", LOCK_EX);
}

$nyers = file_get_contents('php://input') ?: '';
$d = json_decode($nyers, true);
if (!is_array($d)) { vege(['ok' => false], 400); }

/* ── Bejövő értékek szigorú szűrése ── */
$utvonal = mb_substr(trim((string)($d['p'] ?? '/')), 0, 120);
if ($utvonal === '' || $utvonal[0] !== '/') { $utvonal = '/'; }
$utvonal = preg_replace('~[^A-Za-z0-9/._-]~', '', $utvonal) ?: '/';

$hivatkozo = '(közvetlen)';
$ref = trim((string)($d['r'] ?? ''));
if ($ref !== '') {
    $h = parse_url($ref, PHP_URL_HOST);
    if (is_string($h) && $h !== '') {
        $h = strtolower(preg_replace('~[^a-z0-9.-]~i', '', $h) ?: '');
        $sajat = strtolower((string)($_SERVER['HTTP_HOST'] ?? ''));
        $hivatkozo = ($h !== '' && $h !== $sajat && 'www.' . $h !== $sajat && $h !== 'www.' . $sajat)
            ? mb_substr($h, 0, 80) : '(saját oldal)';
    }
}

$sz = (int)($d['w'] ?? 0);
$eszkoz = $sz <= 0 ? 'ismeretlen' : ($sz < 720 ? 'telefon' : ($sz < 1100 ? 'tablet' : 'asztali'));

/* ── Látogató-lenyomat: IP + böngészőazonosító + napi só ── */
$ip  = (string)($_SERVER['REMOTE_ADDR'] ?? '');
$ua  = (string)($_SERVER['HTTP_USER_AGENT'] ?? '');
$jel = substr(hash('sha256', $so . '|' . $ip . '|' . $ua), 0, 16);

/* ── Napi összesítő fájl ── */
$fajl = $dir . '/stat-' . $ma . '.json';
$fp = @fopen($fajl, 'c+');
if (!$fp) { vege(['ok' => false], 500); }
flock($fp, LOCK_EX);
$tart = stream_get_contents($fp);
$s = json_decode($tart ?: '', true);
if (!is_array($s)) {
    $s = ['nap' => $ma, 'megtekintes' => 0, 'oldalak' => [], 'hivatkozok' => [], 'eszkozok' => [], 'latogatok' => []];
}
$s['megtekintes']++;
$s['oldalak'][$utvonal]    = ($s['oldalak'][$utvonal] ?? 0) + 1;
$s['hivatkozok'][$hivatkozo] = ($s['hivatkozok'][$hivatkozo] ?? 0) + 1;
$s['eszkozok'][$eszkoz]    = ($s['eszkozok'][$eszkoz] ?? 0) + 1;
if (!in_array($jel, $s['latogatok'], true)) {
    if (count($s['latogatok']) < 20000) { $s['latogatok'][] = $jel; }
}
ftruncate($fp, 0); rewind($fp);
fwrite($fp, json_encode($s, JSON_UNESCAPED_UNICODE));
flock($fp, LOCK_UN); fclose($fp);

/* ── 400 napnál régebbi fájlok takarítása ── */
if (random_int(1, 200) === 1) {
    foreach (glob($dir . '/stat-*.json') ?: [] as $f) {
        if (@filemtime($f) < time() - 400 * 86400) { @unlink($f); }
    }
}

vege(['ok' => true]);
