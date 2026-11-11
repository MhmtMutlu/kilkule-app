# kilkule-app

Kilkule'nin web sitesi: tanıtım sayfası, gizlilik politikası, kullanım koşulları, KVKK aydınlatma metni, hesap silme ve
destek. Oyun bu sayfaları buradan açar (`AppSettings.legalURL`); eski `mm-apps.com/kilkule/*` adresleri buraya yönlendirir.
GitHub Pages ile yayınlanır: <https://kilkule.mm-apps.com/>

| Sayfa | Türkçe | English |
|---|---|---|
| Tanıtım | `/` | `/en/` |
| Gizlilik politikası | `/gizlilik/` (bağlayıcı) | `/en/privacy/`; çeviriler `/fr/privacy/`, `/de/privacy/`, `/it/privacy/`, `/es/privacy/` |
| Kullanım koşulları | `/kosullar/` (bağlayıcı) | `/en/terms/` |
| KVKK aydınlatma metni | `/kvkk/` | – |
| Hesap silme | `/hesap-silme/` | `/en/delete-account/` |
| Destek | `/destek/` | `/en/support/` |

## Düzenleme
- Metinler: tanıtım sayfası `build.py` içindeki `S` sözlüğünde; hukuk, destek ve hesap silme sayfaları `src/*.md`
  (`build.py` → `DOC_GROUPS`, `DOC_META`; Markdown'ı `md_to_html` çevirir, dış bağımlılık yok).
- Gizlilik politikası (6 dil), kullanım koşulları (tr, en) ve KVKK metni **burada düzenlenmez**: tek kaynak oyun deposunun
  `docs/legal/` klasörü. Değişince: `python3 tools/import_legal.py ../kilkule` (birebir kopyalar) → `python3 build.py`.
  Destek (`src/support.*.md`) ve hesap silme (`src/delete.*.md`) bu sitenindir; politikayla çelişmemeli.
- Oyun bilgisi (çağlar, diyarlar, savunmalar, yetenekler, boss'lar, lig kademeleri, sayılar, vurgu renkleri) elle yazılmaz:
  `data/game.json` oyunun içerik dosyalarından üretilir. Oyun içeriği değişince:
  `python3 tools/export_content.py ../kilkule` → `python3 build.py`.
- Görseller oyunun kendi SVG kütüphanesinden (`kilkule/kule-savunma/svg-varliklar/kutuphane`) `assets/art/` altına
  kopyalanır (zemin dokuları hariç). `export_content.py` sitenin adını andığı her birimin çizimi var mı diye bakar.
- Yayın günü: `build.py` → `APP_ID` (App Store Connect → App Information → Apple ID) ve `APP_STORE_LIVE = True`
  (tek anahtar). App Store rozetleri gerçek bağlantı olur, "Çok yakında" ve test sürümü cümleleri kalkar.
- Derleme: `python3 build.py` (statik HTML'i depo köküne, `sitemap.xml`'i ve `assets/accents.css`'i yazar, bütün iç
  bağlantıları ve sayfa içi çapaları kontrol eder). Derlenmiş HTML de commit'lenir; GitHub Pages ek bir derleme adımı çalıştırmaz.
- Stil: `assets/site.css` (renk, kontur, yarıçap ve yazı tipleri oyunun KilkuleDesign `tokens.json`'ıyla aynı). Her çağ ve
  diyar yalnızca vurgu rengini değiştirir: `assets/accents.css` `build.py` tarafından üretilir; koyu ton beyaz metin ve
  krem zemin için 4,5:1 kontrastı sağlayana kadar laciverte karıştırılır.
- Betik: `assets/site.js` yalnızca iyileştirme yapar (çağ döngüsü, ray düğmeleri); sayfa onsuz da eksiksiz okunur.
  Hareketi Azalt açıksa çağlar kendiliğinden dönmez.
- Ekran görüntüleri `assets/shots/<dil>/` (iPhone 17 Pro Max simülatörü, 9:41 durum çubuğu, oyunun DEBUG başlatma
  argümanları; 660 px genişlik, WebP). Türkçe set 31 Ekim, İngilizce set 30 Ekim derlemesinden.
- Paylaşım görseli: `python3 tools/og.py` (macOS; QuickLook ile çizer) → `assets/og-tr.png`, `assets/og-en.png`.

## Gizlilik
Site çerez, analiz veya üçüncü taraf istek kullanmaz; Baloo 2 ve Nunito yazı tipleri (SIL OFL, Latin + Türkçe altkümesi)
`assets/fonts/` altından sunulur.

## Yayına alma
Settings → Pages → Source: *Deploy from a branch* → Branch: `main` / `(root)`.
Oyun bu alan adındaki sayfaları dile göre kendisi açar; `Config.xcconfig`'te bir şey girmek gerekmez (`KILKULE_*_URL` yalnız
geçersiz kılmak için). App Store Connect'te gizlilik adresi `https://kilkule.mm-apps.com/gizlilik/` (İngilizce yerelleştirmede
`/en/privacy/`), destek adresi `https://kilkule.mm-apps.com/destek/` (`/en/support/`).
