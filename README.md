# kilkule-app

Kilkule'nin web sitesi: tanıtım sayfası, gizlilik politikası, KVKK aydınlatma metni, hesap silme ve destek.
GitHub Pages ile yayınlanır: <https://mhmtmutlu.github.io/kilkule-app/>

| Sayfa | Türkçe | English |
|---|---|---|
| Tanıtım | `/` | `/en/` |
| Gizlilik politikası | `/gizlilik/` | `/en/privacy/` |
| KVKK aydınlatma metni | `/kvkk/` | – |
| Hesap silme | `/hesap-silme/` | `/en/delete-account/` |
| Destek | `/destek/` | `/en/support/` |

## Düzenleme
- Metinler: tanıtım sayfası `build.py` içindeki `S` sözlüğünde, hukuki sayfalar `src/*.html`.
- Oyun bilgisi (çağlar, diyarlar, savunmalar, yetenekler, boss'lar, lig kademeleri, sayılar, vurgu renkleri) elle yazılmaz:
  `data/game.json` oyunun içerik dosyalarından üretilir. Oyun içeriği değişince:
  `python3 tools/export_content.py ../kilkule` → `python3 build.py`.
- Görseller oyunun kendi SVG kütüphanesinden (`kilkule/kule-savunma/svg-varliklar/kutuphane`) `assets/art/` altına
  kopyalanır (zemin dokuları hariç). `export_content.py` sitenin adını andığı her birimin çizimi var mı diye bakar.
- Yayın günü: `build.py` → `APP_ID` (App Store Connect → App Information → Apple ID) ve `APP_STORE_LIVE = True`
  (tek anahtar). App Store rozetleri gerçek bağlantı olur, "Çok yakında" ve test sürümü cümleleri kalkar.
- Derleme: `python3 build.py` (statik HTML'i depo köküne ve `assets/accents.css`'i yazar, bütün iç bağlantıları ve sayfa
  içi çapaları kontrol eder). Derlenmiş HTML de commit'lenir; GitHub Pages ek bir derleme adımı çalıştırmaz.
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
Sonra oyunun `Config.xcconfig` dosyasına:
```
KILKULE_PRIVACY_URL = https:/$()/mhmtmutlu.github.io/kilkule-app/gizlilik/
KILKULE_SUPPORT_URL = https:/$()/mhmtmutlu.github.io/kilkule-app/destek/
```
App Store Connect'te de aynı adresler girilir.
